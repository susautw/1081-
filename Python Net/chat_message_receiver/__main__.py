import argparse
import json
import os
from pathlib import Path
from shutil import get_terminal_size


class Main:
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
                    print(str(e))

    @staticmethod
    def show_data(data: dict, width):
        if data['type'] == 'report':
            if data['status'] == 'error':
                describe = data['describe']
                message = data['message']

                print(f'%{width}s' % f'{describe}: {message}')

        elif data['type'] == 'reflex_message':
            content = data['content']

            print(f'%{width}s' % f'{content}')

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