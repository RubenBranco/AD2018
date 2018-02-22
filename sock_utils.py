import socket as s

def create_tcp_server_socket(address, port, queue_size):
    """Create a TCP socket for a server"""
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(queue_size)
    return sock

def create_tcp_client_socket(address, port):
    """Create TCP Socket for a client"""
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((address, port))
    return sock

def receive_all(socket, length):
    """Receives all packets, with a maximum length of length"""
    try:
        cur = 0
        msg = ''
        stop = False
        while cur < length and not stop:
            msg += socket.recv(1024)
            cur += 1024
            if len(msg) < 1024:
                stop = True
        return msg
    except s.error:
        socket.close()
        raise Exception("Erro durante o recebimento da mensagem")
