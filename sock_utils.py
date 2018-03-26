import socket as s
import traceback


def create_tcp_server_socket(address, port, queue_size):
    """Create a TCP socket for a server"""
    
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    except s.error as e:
        print "Erro ao criar socket: %s" % e

    try:
        sock.bind((address, port))
    except s.error as e:
        print "Erro ao ligar socket: %s" % e
        sock.close()
        traceback.print_exc()
    sock.listen(queue_size)

    return sock


def create_tcp_client_socket(address, port):
    """Create TCP Socket for a client"""
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    except s.error as e:
        print "Erro ao criar socket: %s" % e

    try:
        sock.connect((address, port))
    except s.error as e:
        print "Erro ao conectar o socket: %s" % e
        sock.close()
        traceback.print_exc()

    return sock


def receive_all(socket, length, buffer_size=1024):
    """Receives all packets, with a maximum length of length"""
    try:
        cur = 0
        msg = ''
        stop = False
        while cur < length and not stop:
            msg += socket.recv(buffer_size)
            cur += buffer_size
            if len(msg) < buffer_size:
                stop = True
        return msg
    except s.error as e:
        print "Erro a receber a informação: %s" % e
        socket.close()
        traceback.print_exc()
