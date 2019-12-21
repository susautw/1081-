import argparse
from pathlib import Path
import socket

from coder import Base85Coder
from io_stream.reader import SocketReader
from io_stream.sender import SocketSender
from logger import Logger, ConsoleLogger
from upload_client.file_sender import FileSender


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    args = _arg_parser_factory().parse_args()
    file_path = Path(args.file)

    host = args.host
    port = args.port

    sock.connect((host, port))
    logger: Logger = ConsoleLogger()
    coder = Base85Coder()

    sender = SocketSender(sock, coder)
    reader = SocketReader(sock, coder)

    if not file_path.exists():
        logger.error(f'{str(file_path)} is not exists.')
        exit(-1)

    if file_path.is_file():
        files = [file_path]
        base_path = file_path.parent
    else:
        files = list(file_path.glob('./**/*.*'))
        base_path = file_path

    file_sender = FileSender(sender)

    # show all the files
    logger.log('The following files will be uploaded:')
    for file in files:
        logger.log(str(file))

    proceed = input('proceed?(y/N):').lower() == 'y'
    if not proceed:
        logger.info('Operation stopped by user.')
        exit(0)

    for file in files:
        file_sender.send_file(file, base_path)

    file_sender.close()

    for response in reader.read():
        if response == b'ok':
            logger.info('All file transmission has been done.')
        elif response.startswith(b'error'):
            logger.error(response.decode())
        else:
            logger.error('Unknown error occurred.')
        reader.close()


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('host', type=str)
    parser.add_argument('-p', '--port', type=int, default=8686)
    return parser


if __name__ == '__main__':
    main()
