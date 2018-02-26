#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""
# Zona para fazer imports
import argparse
import sock_utils
import net_client
import signal

# Programa principal


class Client:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.active_flag = True

        signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.active_flag = False

    def client_requests(self):
        while self.active_flag:
            command = raw_input("comando > ")
            if command and command != "exit":
                client_socket = net_client.server(self.host, self.port)
                client_socket.connect()
                response = client_socket.send_receive(command)
                client_socket.close()
                print "Resposta {}".format(response)
            elif command == "exit":
                self.active_flag = False


if __name__ == "__main__":
    description = "Gestor do Cliente"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("host", type=str, metavar="host",
                        help="O ip do servidor fornecedor de recursos")
    parser.add_argument("port", type=int, metavar="port",
                        help="O porto que o cliente se quer ligar")
    parser.add_argument("id", type=int, metavar="id",
                        help="O id único do cliente")
    args = parser.parse_args()
    Client(args.host, args.port, args.id)
