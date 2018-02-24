import socket as s
import argparse
import sock_utils
import sys
import re
from functools import reduce

def server(host, port):
    sock = sock_utils.create_tcp_server_socket(host, port, 2)
    msgs = {}
    id = 0
    while id < 6:
        (conn_sock, addr) = sock.accept()
        print 'ligado a {}'.format(addr)
        msg = sock_utils.receive_all(conn_sock, 50000)
        if re.match("GET [\d]*", msg):
            conn_sock.sendall(msgs[int(msg[4:])])
        elif msg == "LIST":
            if msgs:
                conn_sock.sendall(reduce(lambda acc, y: acc + "," + msgs[y], msgs.keys(), ''))
            else:
                conn_sock.sendall("dicionario vazio")
        else:
            msgs[id] = msg
            conn_sock.sendall("Mensagem posta com id {}".format(id))
            id += 1
        conn_sock.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente")
    parser.add_argument("port", type=int, help="Port the client will use for connection")
    parser.add_argument("host", type=str, help="host it will use")
    args = parser.parse_args()
    server(args.host, args.port)
