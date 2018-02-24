# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""

# zona para fazer importação

from sock_utils import create_tcp_client_socket, receive_all

# definição da classe server 

class server:
    """
    Classe para abstrair uma ligação a um servidor TCP. Implementa métodos
    para estabelecer a ligação, para envio de um comando e receção da resposta,
    e para terminar a ligação
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.socket = create_tcp_client_socket(self.address, self.port)

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        """
        self.socket.sendall(data)
        return receive_all(self.socket, 50000)
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.socket.close()