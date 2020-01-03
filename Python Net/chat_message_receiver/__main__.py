import argparse
import json
import queue
from pathlib import Path
from shutil import get_terminal_size
from time import sleep


class Main:
    executed_command = queue.Queue()

    @staticmethod
    def main():
        args = Main._arg_parser_factory().parse_args()

        file = Path(args.filepath)

        width = get_terminal_size().columns
        width = width if width <= 100 else 100

        close = False
        with file.open('r') as fp:
            while not close:
                try:
                    data = fp.readline()
                    if data != '':
                        close = Main.show_data(json.loads(data.strip()), width)
                except Exception as e:
                    print('error ', str(e))
        sleep(0.01)
        file.unlink()

    @staticmethod
    def show_data(data: dict, width):
        if data['type'] == 'executed_command':
            Main.executed_command.put(data['command'])
        elif data['type'] == 'report':
            if data['status'] == 'ok':
                command = Main.executed_command.get()
                if command != 'message':
                    print(f'%{width}s' % f'{command} ... ok!')
            else:
                describe = data['describe']
                message = data['message']
                Main.executed_command.get()

                print(f'%{width}s' % f'{describe}: {message}')

        elif data['type'] == 'reflex_message':
            content = data['content']

            print(f'%{width}s' % f' => {content}')

        elif data['type'] == 'message':
            from_user = data['from']
            content = data['content']
            msg = f'<{from_user}>: {content}'

            print(f'%-{width}s' % msg)
        else:
            return True
        return False

    @staticmethod
    def _arg_parser_factory():
        parser = argparse.ArgumentParser()
        parser.add_argument('filepath', type=str)
        return parser


if __name__ == '__main__':
    Main.main()