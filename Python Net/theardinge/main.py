import argparse
import threading

import numpy as np


class Main:
    @staticmethod
    def main():
        args = Main.arg_parse_factory().parse_args()
        lock = threading.Lock()

        array = np.ones((args.size,))
        sum_ = AtomicNumber()
        threads = []

        for i in range(args.nt):
            t = SumArray(array, args.size, i, args.nt, sum_, lock)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(sum_.data)

    @staticmethod
    def arg_parse_factory():
        parser = argparse.ArgumentParser()
        parser.add_argument('size', type=int)
        parser.add_argument('nt', type=int)
        return parser


class AtomicNumber(object):
    data: int = 0


class SumArray(threading.Thread):
    data: np.array
    size: int
    idx: int
    number_of_threads: int
    sum: AtomicNumber
    lock: threading.Lock

    def __init__(self, data, size, idx, number_of_threads, sum_, lock):
        super().__init__()
        self.data = data
        self.size = size
        self.idx = idx
        self.number_of_threads = number_of_threads
        self.sum = sum_
        self.lock = lock

    def run(self):
        chunk_size = self.size // self.number_of_threads
        low = chunk_size * self.idx
        high = chunk_size * (self.idx + 1)
        r = self.size % self.number_of_threads

        if self.idx >= self.number_of_threads - r:
            offset = self.idx - self.number_of_threads + r
            low += offset
            high += offset + 1

        local_sum = 0
        for x in self.data[low:high]:
            local_sum += x

        self.lock.acquire()
        print(f'{self.idx}:[{low}, {high}) --> {local_sum}')
        self.sum.data += local_sum
        self.lock.release()
