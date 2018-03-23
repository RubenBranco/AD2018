#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_server.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""

# Zona para fazer importação
import sock_utils
import argparse
import socket as s
import struct
import pickle
from lock_skel import *
import SocketServer
import select as sel
import signal

###############################################################################

# código do programa principal

class MessageHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        addr, port = self.request.getpeername()
        print "Ligado a cliente com IP {} e porto {}".format(addr, port)
        
    def handle(self):
        global skeleton
        continue_flag = True
        while continue_flag:
            r, w, x = sel.select([self.request], [], [])
            for sock in r:
                size = sock_utils.receive_all(sock, 4, 4)
                if size:
                    skeleton.clear_expired_locks()
                    skeleton.clear_maxed_locks()
                    rcv_message_size = struct.unpack("!i", size)[0]
                    rcv_message = pickle.loads(sock_utils.receive_all(
                        sock, rcv_message_size))
                    self.client_message_handler(sock, rcv_message)
                else:
                    addr, port = sock.getpeername()
                    print "Cliente com IP {} e porto {} fechou a ligação".format(addr, port)
                    sock.close()
                    continue_flag = False

    def client_message_handler(self, conn_sock, rcv_message):
        """
        Processa uma mensagem recebida por um cliente e retorna uma resposta para
        o cliente.
        """
        global skeleton
        response = skeleton.message_parser(rcv_message)
        response_obj = pickle.dumps(response)
        size = struct.pack("!i", len(response_obj))
        try:
            conn_sock.sendall(size)
            conn_sock.sendall(response_obj)
        except s.error:
            conn_sock.close()
        finally:
            skeleton.print_lock_state()


class Server:
    def __init__(self, port, N, K, Y, T):
        """
        Define um TCP Server e um lock pool, recebendo pedidos de clientes
        que têm o fim de manipular locks de recursos na lock pool.
        *args descritos na classe lock_pool.
        """
        self.port = port
        self.tcp_server = SocketServer.ThreadingTCPServer(('127.0.0.1', port), MessageHandler)
        
        global skeleton
        skeleton = LockSkeleton(N, K, Y, T)

        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def serve_forever(self):
        """
        Serve clientes eternamente, satisfazendo os pedidos
        (até um evento CTRL+C)
        """
        self.tcp_server.serve_forever()

    def shutdown(self, signal, frame):
        self.tcp_server.shutdown()


if __name__ == "__main__":
    description = "Servidor TCP para gestão de exclusão mútua de recursos."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("port", type=int, metavar="port",
                        help="Porto em que o servidor irá correr")
    parser.add_argument("N", type=int, metavar="N",
                        help="Número de recursos que serão geridos pelo servidor.")
    parser.add_argument("K", type=int, metavar="K",
                        help="Número de bloqueios permitidos de cada recurso.")
    parser.add_argument("Y", type=int, metavar="Y",
                        help="Número permitido de recursos bloqueados num dado momento.")
    parser.add_argument("T", type=int, metavar="T",
                        help="Tempo de concessão (em segundos) dos bloqueios.")
    args = parser.parse_args()
    lock_server = Server(args.port, args.N, args.K, args.Y, args.T)
    lock_server.serve_forever()
