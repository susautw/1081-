import os
from pathlib import Path
from time import sleep


def main():
    f = Path('client.tmp')

    i = 0
    with f.open('w') as fp:
        while True:
            sleep(0.01)
            fp.write(f'a{i}\n')
            fp.flush()
            i += 1


if __name__ == '__main__':
    main()
