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

# Programa principal
class Client:
	def __init__(self,host,port,client_id):
		self.host = args.host
		self.port = args.port
		self.client_id = args.id
	
	def client_requests(self,host, port):
                self.host = host
                self.port = port
		active = True
		while active:
			command = raw_input("comando > ")
			if command:
				client_socket = sock_utils.creat_tcp_client_socket(host,port)
			if command == "exit":
				active = false
			else: 
				client_socket.sendall(command)
			resposta = sock.utils.receive_all(client_socket, 5000)
                        print "Rsposta {}".format(resposta)




if __name__ == "__main__":
	description = "Gestor do Cliente"
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument("host", type = str, metavar = "host", help = "O ip do servidor fornecedor de recursos")
	parser.add_argument("port", type = int, metavar="port", help = "O porto que o cliente se quer ligar")
	parser.add_argument("id do cliente", type = int, metavar = "id do cliente", help = "O id único do cliente")
	args = parser.parse_args()


