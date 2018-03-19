#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""
# Zona para fazer imports
import argparse
from lock_stub import *
import re

# Programa principal


class Client:
    def __init__(self, host, port, client_id):
        """
        Instância as variaveis necessárias para o cliente

        Host é um IP de acesso ao servidor
        Port é a port usada pelo servidor
        client_id é um id ÚNICO de cliente
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.active_flag = True
    
    def message_parser(self, message):
        ret = "UNKNOWN COMMAND"
        if re.match("LOCK \d+", message):
            resource_id = re.findall("LOCK (\d+)", message)[0]
            ret = self.stub.lock(self.client_id, int(resource_id))
        elif re.match("RELEASE \d+", message):
            resource_id = re.findall("LOCK (\d+)", message)[0]
            ret = self.stub.release(self.client_id, int(resource_id))
        elif re.match("TEST \d+", message):
            resource_id = re.findall("TEST (\d+)", message)[0]
            ret = self.stub.test(int(resource_id))
        elif re.match("STATS \d+", message):
            resource_id = re.findall("STATS (\d+)", message)[0]
            ret = self.stub.stats(int(resource_id))
        elif re.match("STATS-Y", message):
            ret = self.stub.stats_y()
        elif re.match("STATS-N", message):
            ret = self.stub.stats_n()
        return ret

    def client_requests(self):
        """
        Recebe comandos de cliente e envia-os para o servidor,
        recebendo a resposta e mostrando-a.
        """
        self.stub = LockStub()
        self.stub.connect(self.host, self.port)
        while self.active_flag:
            command = raw_input("comando > ")
            if command and command != "exit":
                ret = self.message_parser(command)
                print(ret)
            elif command == "exit":
                self.active_flag = False
        self.stub.disconnect()


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
    client = Client(args.host, args.port, args.id)
    client.client_requests()
