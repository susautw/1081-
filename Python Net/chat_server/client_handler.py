import json
from abc import ABC, abstractmethod
from typing import Dict

from chat_server.error import IllegalOperation, UserAlreadyExists, UserNotExists, RoomAlreadyExists, RoomNotExists, \
    IncorrectPassword
from chat_server.models import User, Room
from io_stream.sender import Sender
from logger import Logger
from patterns import Singleton


class ClientHandler:
    """
    All property is plaintext.
    The Application handles a single user(client).
    """

    _state: 'ClientHandlerState'
    sender: Sender
    logger: Logger

    # User related
    username: str
    password: str

    user: User = None

    # Room related
    name: str

    room: Room = None

    # Message related
    message: str
    chatting_clients: Dict[User, 'ClientHandler'] = {}

    def __init__(self, sender: Sender, logger: Logger):
        self._state = Waiting()
        self.sender = sender
        self.logger = logger

    @property
    def state(self) -> 'ClientHandlerState':
        return self._state

    @state.setter
    def state(self, state: 'ClientHandlerState') -> None:
        self._state = state

    def register(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.state.register(self)

    def login(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.state.login(self)

    def logout(self) -> None:
        self.state.logout(self)

    def create(self, name: str) -> None:
        self.name = name
        self.state.create(self)

    def join(self, name: str) -> None:
        self.name = name
        self.state.join(self)

    def leave(self) -> None:
        self.state.leave(self)

    def send_message(self, message: str) -> None:
        self.message = message
        self.state.send_message(self)

    def close(self) -> None:
        self.state.close(self)

    @property
    def user_is_alive(self) -> bool:
        return not self.sender.is_closed()

    @staticmethod
    def close_all_disconnected_user() -> None:
        for handler in ClientHandler.chatting_clients.values():
            if not handler.user_is_alive:
                handler.close()


class ClientHandlerState(ABC, Singleton):

    @abstractmethod
    def register(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def login(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def logout(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def create(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def join(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def leave(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def send_message(self, ctx: ClientHandler):
        pass

    @abstractmethod
    def close(self, ctx: ClientHandler):
        pass


class AbstractClientHandlerState(ClientHandlerState):
    def register(self, ctx: ClientHandler):
        self.illegal_operation()

    def login(self, ctx: ClientHandler):
        self.illegal_operation()

    def logout(self, ctx: ClientHandler):
        self.illegal_operation()

    def create(self, ctx: ClientHandler):
        self.illegal_operation()

    def join(self, ctx: ClientHandler):
        self.illegal_operation()

    def leave(self, ctx: ClientHandler):
        self.illegal_operation()

    def send_message(self, ctx: ClientHandler):
        self.illegal_operation()

    def close(self, ctx: ClientHandler):
        self.illegal_operation()

    @staticmethod
    def illegal_operation():
        raise IllegalOperation()

    @staticmethod
    def _send_response(ctx: ClientHandler, data: Dict) -> None:
        if ctx.user_is_alive:
            ctx.sender.send(json.dumps(data).encode())

    @staticmethod
    def _board_cast(ctx: ClientHandler, msg: str):
        data = {
            'type': 'message',
            'from': ctx.user.username,
            'content': msg
        }
        json_data = json.dumps(data).encode()

        ClientHandler.close_all_disconnected_user()
        for user in ctx.room.users:
            if user != ctx.user:
                ctx.chatting_clients[user].sender.send(json_data)


class Waiting(AbstractClientHandlerState):
    def register(self, ctx: ClientHandler):
        if User.has_user(ctx.username):
            raise UserAlreadyExists(ctx.username)

        user = User(ctx.username, ctx.password)
        user.store()

        response = {
            'type': 'report',
            'status': 'ok'
        }

        self._send_response(ctx, response)

    def login(self, ctx: ClientHandler):
        if not User.has_user(ctx.username):
            raise UserNotExists(ctx.username)

        user = User.find(ctx.username)
        if user.password != ctx.password:
            raise IncorrectPassword()

        ctx.user = user
        ctx.state = LoggedIn()
        ctx.chatting_clients[ctx.user] = ctx

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def close(self, ctx: ClientHandler):
        ctx.state = Closed()
        ctx.close()


class LoggedIn(AbstractClientHandlerState):
    def create(self, ctx: ClientHandler):
        if Room.has_room(ctx.name):
            raise RoomAlreadyExists(ctx.name)

        room = Room(ctx.name)
        room.store()

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def join(self, ctx: ClientHandler):
        if not Room.has_room(ctx.name):
            raise RoomNotExists(ctx.name)

        room = Room.find(ctx.name)
        room.add_user(ctx.user)
        ctx.room = room
        ctx.state = Chatting()

        self._board_cast(ctx, f'User {ctx.user.username} has joined this room.')

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def logout(self, ctx: ClientHandler):
        ctx.chatting_clients.pop(ctx.user)
        ctx.state = Waiting()

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def close(self, ctx: ClientHandler):
        ctx.logout()
        ctx.close()


class Chatting(AbstractClientHandlerState):
    def send_message(self, ctx: ClientHandler):
        self._board_cast(ctx, ctx.message)

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def leave(self, ctx: ClientHandler):
        self._board_cast(ctx, f'{ctx.user.username} has left this room.')

        ctx.room.remove_user(ctx.user)
        ctx.state = LoggedIn()

        response = {
            'type': 'report',
            'status': 'ok'
        }
        self._send_response(ctx, response)

    def close(self, ctx: ClientHandler):
        ctx.leave()
        ctx.logout()
        ctx.close()


class Closed(AbstractClientHandlerState):
    def close(self, ctx: ClientHandler):
        ctx.sender.close()
