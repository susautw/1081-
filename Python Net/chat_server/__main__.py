import argparse


class Main:
    @staticmethod
    def main() -> None:
        args = Main._arg_parser_factory().parse_args()

    @staticmethod
    def _arg_parser_factory() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        return parser


if __name__ == '__main__':
    Main.main()
