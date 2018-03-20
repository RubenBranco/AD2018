#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 2 - lock_skel.py
Grupo: ad007
Números de aluno: 50006, 50013, 50019
"""

from lock_pool import *
from multiprocessing import Semaphore


class LockSkeleton:
    def __init__(self, N, K, Y, T):
        self.lock_pool = lock_pool(N, K, Y, T)
        self.T = T
        self.sem = Semaphore(1)

    def message_parser(self, message):
        code = message[0]

        if code == 10:
            return self.lock(message[1], message[2])
        elif code == 20:
            return self.release(message[1], message[2])
        elif code == 30:
            return self.test(message[1])
        elif code == 40:
            return self.stats(message[1])
        elif code == 50:
            return self.stats_y()

        return self.stats_n()

    def lock(self, client_id, resource_id):
        code = 11
        exit_response = None

        if self.lock_pool.exists(resource_id):
            self.sem.acquire()
            exit_response = self.lock_pool.lock(
                resource_id, client_id, self.T)
            self.sem.release()

        return [code, exit_response]

    def release(self, client_id, resource_id):
        code = 21
        exit_response = None

        if self.lock_pool.exists(resource_id):
            self.sem.acquire()
            exit_response = self.lock_pool.release(
                resource_id, client_id)
            self.sem.release()

        return [code, exit_response]

    def test(self, resource_id):
        code = 31
        exit_response = None

        if self.lock_pool.exists(resource_id):
            self.sem.acquire()
            lock_test = self.lock_pool.test(resource_id)
            self.sem.release()
            if lock_test:
                exit_response = True
            else:
                # É necessário fazer um teste extra pois o metodo test
                # da classe lock pool é ambiguo quando retorna false
                # podendo ter 2 possibilidades(inativo ou locked)
                self.sem.acquire()
                status = self.lock_pool.locks[resource_id].test()
                self.sem.release()
                if status == "Inativo":
                    exit_response = "disable"
                else:
                    exit_response = False

        return [code, exit_response]

    def stats(self, resource_id):
        code = 41
        exit_response = None

        if self.lock_pool.exists(int(resource_id)):
            self.sem.acquire()
            stat_num = self.lock_pool.stat(resource_id)
            self.sem.release()
            exit_response = stat_num

        return [code, exit_response]

    def stats_y(self):
        code = 51
        exit_response = self.lock_pool.stat_y()
        return [code, exit_response]
    
    def stats_n(self):
        code = 61
        exit_response = self.lock_pool.stat_n()
        return [code, exit_response]

    def clear_expired_locks(self):
        self.lock_pool.clear_expired_locks()
    
    def clear_maxed_locks(self):
        self.lock_pool.clear_maxed_locks()
