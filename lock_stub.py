#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""

import net_client

class LockStub:

    def __init__(self):
        self.socket = None

    def connect(self, host, port):
        self.socket = net_client.server(host, port)
    
    def disconnect(self):
        self.socket.close()

    def lock(self, client_id, resource_id):
        code = 10
        return self.socket.send_receive([code, client_id, resource_id])

    def release(self, client_id, resource_id):
        code = 20
        return self.socket.send_receive([code, client_id, resource_id])

    def test(self, resource_id):
        code = 30
        return self.socket.send_receive([code, resource_id])

    def stats(self, resource_id):
        code = 40
        return self.socket.send_receive([code, resource_id])
    
    def stats_y(self):
        code = 50
        return self.socket.send_receive([code])

    def stats_n(self):
        code = 60
        return self.socket.send_receive([code])