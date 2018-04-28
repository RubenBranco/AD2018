# -*- coding:utf-8 -*-
from __future__ import print_function
import requests
import re


def handle_requests():
    stop = False
    while not stop:
        cmd = raw_input("Comando? ")
        if cmd and cmd != 'exit':
            response = message_parser(cmd)
            response_parser(response)
        elif cmd == 'exit':
            stop = True


def response_parser(response):
    print(response)


def message_parser(message):
    """
    Verifica a mensagem recebida e interpreta-a
    """
    # TODO fazer as transformacoes para json e passar como dados para enviar ao servidor
    ret = "UNKNOWN COMMAND"
    elements = message.split()

    if re.match(r"ADD USER [A-Za-z]+ [A-Za-z\d]+ [A-Za-z\d]+", message):
        return requests.post("http://localhost:5000/utilizadores", data={"name": elements[2], "username": elements[3], "password": elements[4]})
    elif re.match(r"ADD SERIE [A-Za-z]+ [\d]{4}-[\d]{2}-[\d]{2} [A-Za-z\d]+ [\d]+", message):
        return requests.post("http://localhost:5000/series", data={"name": elements[2], "start_date": elements[3], "synopse": elements[4], "category": elements[5]})
    elif re.match(r"ADD EPISODIO [A-Za-z\d]+ [A-Za-z\d]+ \d+", message):
        return requests.post('http://localhost:5000/episodios', data={"name": elements[2], "description": elements[3], "serie_id": int(elements[4])})
    elif re.match(r"ADD \d+ \d+ [A-Z]{1,2}", message):
        return requests.post('http://localhost:5000/series/' + elements[2], data={"user_id": int(elements[1]), "classification": elements[3]})

    elif re.match(r"REMOVE USER \d+", message):
        return requests.delete('http://localhost:5000/utilizadores/' + elements[2])
    elif re.match(r"REMOVE SERIE \d+", message):
        return requests.delete('http://localhost:5000/series/' + elements[2])
    elif re.match(r"REMOVE EPISODIO \d+", message):
        return requests.delete('http://localhost:5000/episodios/' + elements[2])
    elif re.match(r"REMOVE ALL USERS", message):
        return requests.delete('http://localhost:5000/utilizadores')
    elif re.match(r"REMOVE ALL SERIE", message):
        return requests.delete('http://localhost:5000/series')
    elif re.match(r"REMOVE ALL EPISODIO", message):
        return requests.delete('http://localhost:5000/episodios')
    elif re.match(r"SHOW ALL SERIE_U \d+", message):
        return requests.get('http://localhost:5000/series', data={"op": elements[2]})
    elif re.match(r"SHOW ALL SERIE_C \d+", message):
        return requests.get('http://localhost:5000/series', data={"op": elements[2]})
    elif re.match(r"REMOVE ALL EPISODIO \d+", message):
        return requests.delete('http://localhost:5000/series/' + elements[3])

    elif re.match(r"SHOW USER \d+", message):
        return requests.get('http://localhost:5000/utilizadores/' + elements[2])
    elif re.match(r"SHOW SERIE \d+", message):
        return requests.get('http://localhost:5000/series/' + elements[2])
    elif re.match(r"SHOW EPISODIO \d+", message):
        return requests.get('http://localhost:5000/episodios/' + elements[2])
    elif re.match(r"SHOW ALL USERS", message):
        return requests.get('http://localhost:5000/utilizadores')
    elif re.match(r"SHOW ALL SERIE", message):
        return requests.get('http://localhost:5000/series')
    elif re.match(r"SHOW ALL EPISODIO", message):
        return requests.get('http://localhost:5000/episodios')
    elif re.match(r"SHOW ALL SERIE_U \d+", message):
        return requests.get('http://localhost:5000/series', data={"op": elements[2]})
    elif re.match(r"SHOW ALL SERIE_C \d+", message):
        return requests.get('http://localhost:5000/series', data={"op": elements[2]})
    elif re.match(r"SHOW ALL EPISODIO \d+", message):
        return requests.get('http://localhost:5000/series/' + elements[3])

    elif re.match(r"UPDATE SERIE \d+ \d+ [A-Z]{1,2}", message):
        return requests.patch('http://localhost:5000/series/' + elements[3], data={"serie_id": int(elements[2]), "classification": elements[4]})
    elif re.match(r"UPDATE USER \d+ [A-Za-z\d]+", message):
        return requests.patch('http://localhost:5000/series/' + elements[2], data={"password": elements[3]})

    return ret


if __name__ == "__main__":
    handle_requests()
