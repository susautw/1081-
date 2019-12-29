import json
from abc import ABC, abstractmethod
from typing import List, Dict

from patterns import Serializable


class Command(ABC, Serializable):
    """
    when all subclasses performing serialize, need to add a 'type' to refer to own class name.
    """
    all_command: Dict = {

    }

    @abstractmethod
    def execute(self):
        pass


class CommandInvoker(Serializable):
    commands: List[Command]

    def __init__(self):
        self.commands = []

    def store_command(self, command: Command) -> None:
        self.commands.append(command)

    def send_all(self):
        for command in self.commands:
            command.execute()

    def serialize(self) -> bytes:
        data = [command.serialize() for command in self.commands]
        return json.dumps(data).encode()

    def unserialize(self, serialized: bytes):
        data = [Command.all_command[command['type']]().unserialize() for command in json.loads(serialized.decode())]
        self.commands = data
