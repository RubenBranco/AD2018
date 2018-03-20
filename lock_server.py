#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""

# Zona para fazer importação
import time
import sock_utils
import argparse
import signal
import re
import socket as s
from multiprocessing import Semaphore
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

        signal.signal(signal.SIGINT, self.event_handler)  # CTRL+C Handler

    def event_handler(self, sig, frame):
        """
        Muda o valor da flag active_flag para False, proveniente de um evento
        de CTRL+C assinalando o fim da atividade do servidor.
        """
        self.active_flag = False

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
        while self.active_flag:
            r, w, x = sel.select(socket_list, [], [])
            for sock in r:
                if sock is self.tcp_server:
                    conn_sock, addr = sock.accept()
                    print "Ligado a cliente com IP {} e porto {}".format(
                    addr[0], addr[1])
                    socket_list.append(conn_sock)
                else:
                    
            try:

                conn_sock, addr = self.tcp_server.accept()
                print "Ligado a cliente com IP {} e porto {}".format(
                    addr[0], addr[1])
                self.lock_pool.clear_expired_locks()  # Recursos cujo tempo expirou
                self.lock_pool.clear_maxed_locks()  # Recursos que atingiram maximo de bloqueios
                size = sock_utils.receive_all(conn_sock, 4, 4)
                rcv_message_size = struct.unpack("!i", size)[0]
                rcv_message = sock_utils.receive_all(
                    conn_sock, rcv_message_size)
                thread = Thread(target=self.client_message_handler, args=(conn_sock, pickle.loads(rcv_message)))
                thread.start()
            except s.error as e:
                conn_sock.close()
        self.tcp_server.close()


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
