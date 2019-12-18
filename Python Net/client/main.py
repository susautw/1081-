from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


def main(argv):
    (SERVER, PORT) = ('127.0.0.1', 9999)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((SERVER, PORT))
    s.send(b'Hello, world')
    data = s.recv(1024)
    s.close()
    print('Received', data)


def UDPmain(argv):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('127.0.0.1', 0))
    print("using", sock.getsockname())
    server = ('140.128.3.163', 12333)
    sock.sendto("Mixed Case String owo".encode(), server)
    data, address = sock.recvfrom(1024)
    print("Received", data.decode(), "from", address)

