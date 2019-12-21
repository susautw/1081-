import time
import threading


def main():
    t = threading.Thread(target=thread_test, args=())
    t.start()
    t2 = threading.Thread(target=thread_test, args=())
    t2.start()
    t3 = threading.Thread(target=thread_test, args=())
    t3.start()
    time.sleep(0.2)
    print(threading.active_count())


def thread_test():
    pass


if __name__ == '__main__':
    main()