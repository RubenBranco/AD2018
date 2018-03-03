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
import struct
import pickle

###############################################################################


class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.status = 'Inativo'
        self.num_blocks = 0
        self.client = None
        self.time_valid = None

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if self.status == 'Desbloqueado' or (self.status == 'Bloqueado' and self.client == client_id):
            self.status = 'Bloqueado'
            self.num_blocks += 1
            self.client = client_id
            self.time_valid = time_limit
            return True
        return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.status = 'Desbloqueado'
        self.client = None
        self.time_valid = None

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if client_id == self.client:
            self.urelease()
            return True
        return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se 
        encontre inativo.
        """
        return self.status

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.num_blocks

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.urelease()
        self.status = 'Inativo'


###############################################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao 
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado 
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um 
        recurso seja libertado.
                Define T, o tempo máximo de concessão de bloqueio.
        """
        self.locks = [resource_lock() for _ in range(N)]
        self.N = N
        self.K = K
        self.Y = Y
        self.num_blocked = 0
        self.T = T

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        time_now = time.time()
        for lock in self.locks:
            if lock.time_valid < time_now:
                lock.urelease()

    def __try_lock__(self, resource_id, client_id, time_limit):
        status = self.locks[resource_id].test()
        if status != 'Inativo' and self.stat_y() < self.Y:
            return True
        return False

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não 
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi 
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        if self.__try_lock__(resource_id, client_id, time_limit):
            lock_return = self.locks[resource_id].lock(
                client_id, time.time() + self.T)
            if lock_return:
                self.num_blocked += 1
            return lock_return
        return False

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        release_return = self.locks[resource_id].release(client_id)
        if release_return:
            self.num_blocked -= 1
        return release_return

    def test(self, resource_id):
        """
        Retorna True se o recurso resource_id estiver desbloqueado e False caso 
        esteja bloqueado ou inativo.
        """
        resource_status = self.locks[resource_id].test()
        if resource_status == 'Desbloqueado':
            return True
        return False

    def stat(self, resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos 
        K bloqueios permitidos.
        """
        return self.locks[resource_id].stat()

    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        return self.num_blocked

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        return self.N - self.num_blocked

    def clear_maxed_locks(self):
        """
        Verifica se os recursos não excederam o limite permitido de bloqueios.
        Se tiverem, são desativados.
        """
        for i in range(len(self.locks)):
            num_blocks = self.stat(i)
            if num_blocks >= self.K and self.test(i):
                self.locks[i].disable()

    def exists(self, resource_id):
        return resource_id < len(self.locks)

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso não esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #
        for i in range(len(self.locks)):
            status = self.locks[i].test()
            if status == "Inativo" or status == "Desbloqueado":
                output += "recurso {} {}\n".format(i, status.lower())
            else:
                output += "recurso {} bloqueado pelo cliente {} até {}\n".format(
                    i, self.locks[i].client, time.ctime(self.locks[i].time_valid))

        return output

###############################################################################

# código do programa principal


class Server:
    def __init__(self, port, N, K, Y, T):
        self.port = port
        self.lock_pool = lock_pool(N, K, Y, T)
        self.tcp_server = sock_utils.create_tcp_server_socket(
            '127.0.0.1', port, 1)
        self.active_flag = True
        self.sem = Semaphore(1)
        self.T = T

        signal.signal(signal.SIGINT, self.event_handler)

    def event_handler(self, sig, frame):
        self.active_flag = False

    def client_message_handler(self, conn_sock, rcv_message):
        """
        Retorna uma lista com a mensagem dividida nos seguintes parametros [comando recebido, 1º, 		2ºargumento, ....]
        """
        res = ''
        if re.match("LOCK \d+ \d+", rcv_message):
            client_id, resource_id = re.findall(
                "LOCK (\d+) (\d+)", rcv_message)[0]
            if self.lock_pool.exists(int(resource_id)):
                self.sem.acquire()
                ret = self.lock_pool.lock(int(resource_id), int(client_id), self.T)
                self.sem.release()
                res = ("OK" if ret else "NOK")
            else:
                res = "UNKNOWN RESOURCE"

        elif re.match("RELEASE (\d+) (\d+)", rcv_message):
            client_id, resource_id = re.findall("RELEASE (\d+) (\d+)",
                                                rcv_message)[0]
            if self.lock_pool.exists(int(resource_id)):
                self.sem.acquire()
                exit_code = self.lock_pool.release(
                    int(resource_id), int(client_id))
                self.sem.release()
                res = ("OK" if exit_code else "NOK")
            else:
                res = "UNKNOWN RESOURCE"

        elif re.match("TEST \d+", rcv_message):
            resource_id = re.findall("TEST (\d+)", rcv_message)[0]
            if self.lock_pool.exists(int(resource_id)):
                self.sem.acquire()
                lock_test = self.lock_pool.test(int(resource_id))
                self.sem.release()
                if lock_test:
                    res = "UNLOCKED"
                else:
                    self.sem.acquire()
                    status = self.lock_pool.locks[int(resource_id)].test()
                    self.sem.release()
                    if status == "Inativo":
                        res = "DISABLE"
                    else:
                        res = "LOCKED"
            else:
                res = "UNKNOWN RESOURCE"

        elif re.match("STATS \d+", rcv_message):
            resource_id = re.findall("STATS (\d+)", rcv_message)[0]
            if self.lock_pool.exists(int(resource_id)):
                self.sem.acquire()
                stat_num = self.lock_pool.stat(int(resource_id))
                self.sem.release()
                res = str(stat_num)
            else:
                res = "UNKNOWN RESOURCE"

        elif re.match("STATS-Y", rcv_message):
            self.sem.acquire()
            stat_y = self.lock_pool.stat_y()
            self.sem.release()
            res = str(stat_y)

        elif re.match("STATS-N", rcv_message):
            self.sem.acquire()
            stat_n = self.lock_pool.stat_n()
            self.sem.release()
            res = str(stat_n)

        else:
            res = "UNKOWN COMMAND"
        try:
            res_obj = pickle.dumps(res, -1)
            res_size = struct.pack("!i", len(res_obj))
            conn_sock.sendall(res_size)
            conn_sock.sendall(res_obj)
        except s.error as e:
            pass
        finally:
            conn_sock.close()

    def serve_forever(self):
        while self.active_flag:
            try:
                conn_sock, addr = self.tcp_server.accept()
                print "Ligado a cliente com IP {} e porto {}".format(
                    addr[0], addr[1])
                self.lock_pool.clear_expired_locks()
                self.lock_pool.clear_maxed_locks()
                size = sock_utils.receive_all(conn_sock, 4, 4)
                rcv_message_size = struct.unpack("!i", size)[0]
                rcv_message = sock_utils.receive_all(conn_sock, rcv_message_size)
                self.client_message_handler(conn_sock, pickle.loads(rcv_message))
                print self.lock_pool
            except s.error as e:
                pass
            finally:
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
