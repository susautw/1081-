import argparse


def main():
    args = _arg_parser_factory().parse_args()

    port = args.port


def _arg_parser_factory():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7086)
    return parser


if __name__ == '__main__':
    main()
