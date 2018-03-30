#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket as s


def create_tcp_server_socket(address, port, queue_size):
    """
    Cria um socket TCP para servidor.
    """
    
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    except s.error:
        print "Erro ao criar socket de servidor"

    try:
        sock.bind((address, port))
    except s.error:
        print "Erro ao tentar ligar ao IP e porto, pode ainda estar em uso"
        sock.close()
    sock.listen(queue_size)

    return sock


def create_tcp_client_socket(address, port):
    """
    Cria um socket TCP para cliente.
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    except s.error:
        print "Erro ao criar socket de cliente"

    try:
        sock.connect((address, port))

    except s.error:
        print "Erro ao tentar conectar com o servidor."
        sock.close()

    return sock


def receive_all(socket, length, buffer_size=1024):
    """
    Recebe todos os pacotes, com um tamanho total definido.
    """
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
    except s.error:
        print "Erro ao receber dados."
        socket.close()
