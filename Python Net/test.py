import random


def main():
    li = [random.randint(0, 1) for _ in range(100)]

    for i, e in enumerate(li):
        print(e, end=' ')
        if i % 10 == 9 and i != len(li) - 1:
            print()
    print('\n')
    print(f'Total {len(list(filter(lambda x: x == 0, li)))} zeros in li')


if __name__ == '__main__':
    main()
