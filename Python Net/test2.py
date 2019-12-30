from pathlib import Path


def main():
    f = Path('client.tmp')
    with f.open('r') as fp:
        while True:
            data = fp.readline()
            if data != '':
                print(data)


if __name__ == '__main__':
    main()