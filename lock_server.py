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
from threading import Thread
import struct
import pickle
from lock_skel import *
import select as sel

###############################################################################

# código do programa principal


class Server:
    def __init__(self, port, N, K, Y, T):
        """
        Define um TCP Server e um lock pool, recebendo pedidos de clientes
        que têm o fim de manipular locks de recursos na lock pool.
        *args descritos na classe lock_pool.
        """
        self.port = port
        self.lock_pool = lock_pool(N, K, Y, T)
        self.tcp_server = sock_utils.create_tcp_server_socket(
            '127.0.0.1', port, 1)
        self.active_flag = True
        self.sem = Semaphore(1)  # Semaforo para limite de acessos concorrentes
        self.T = T
        self.skeleton = LockSkeleton(N, K, Y, T)

    def client_message_handler(self, conn_sock, rcv_message):
        """
        Processa uma mensagem recebida por um cliente e retorna uma resposta para
        o cliente.
        """
        response = self.skeleton.message_parser(rcv_message)
        response_obj = pickle.dumps(response)
        size = struct.pack("!i", len(response_obj))
        try:
            conn_sock.sendall(size)
            conn_sock.sendall(response_obj)
        except s.error:
            conn_sock.close()

    def serve_forever(self):
        """
        Serve clientes eternamente, satisfazendo os pedidos
        (até um evento CTRL+C)
        """
        socket_list = [self.tcp_server]
        thread_workers = []
        while self.active_flag:
            r, w, x = sel.select(socket_list, [], [])
            for i, sock in enumerate(r):
                if sock is self.tcp_server:
                    conn_sock, addr = sock.accept()
                    print "Ligado a cliente com IP {} e porto {}".format(
                        addr[0], addr[1])
                    socket_list.append(conn_sock)
                    thread_workers.append(Thread())
                else:
                    self.skeleton.clear_expired_locks()
                    self.skeleton.clear_maxed_locks()
                    
                    size = sock_utils.receive_all(sock, 4, 4)
                    if size:
                        rcv_message_size = struct.unpack("!i", size)[0]
                        rcv_message = pickle.loads(sock_utils.receive_all(
                            sock, rcv_message_size))
                        thread = thread_workers[i]
                        thread.target = self.client_message_handler
                        thread.args = (sock, rcv_message)
                        thread.start()
                    else:
                        addr, port = sock.getpeername()
                        print "Cliente com IP {} e porto {} fechou a ligação".format(addr, port)
                        sock.close()
                        socket_list.remove(sock)
                        del thread_workers[i]

        map(lambda sock: sock.close(), socket_list)


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
