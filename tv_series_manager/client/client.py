# -*- coding:utf-8 -*-
from __future__ import print_function
import requests
import re
import json
import os
from requests_oauthlib import OAuth2Session


def establish_session(session, token):
    return token_response(session.post("https://localhost:5000/token", data=json.dumps({"token": token})))


def get_oauth_token():
     # Credenciais obtidas da API github no registo da aplicacao
    client_id = 'd58498b6e10353206e26'
    client_secret = 'c6a8aca3d7e69b7a69a7d90e70d259902e9a7f3d'

    # Servidores da github para obtencao do authorization_code e do token
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'
    github = OAuth2Session(client_id)

    authorization_url, state = github.authorization_url(authorization_base_url)
    print('Aceder ao link (via browser) para obter a autorizacao,', authorization_url)

    # Obter o authorization_code do servidor vindo no URL de redireccionamento
    redirect_response = raw_input(
        ' insira o URL devolvido no browser e cole aqui:')

    # Obtencao do token
    token = github.fetch_token(
        token_url, client_secret=client_secret, authorization_response=redirect_response)

    return token


def handle_requests():
    """
    Obtem token e obtem comandos do utilizador para mandar para o cliente.
    """

    token = get_oauth_token()

    authorized = False
    client_id = 0

    session = requests.Session()
    session.cert = [os.path.join("..", "certs", "client.crt"),
                    os.path.join("..", "certs", "client.key")]
    session.verify = os.path.join("..", "certs", "root.pem")

    stop = False
    while not stop:
        cmd = raw_input("Comando? ")
        if cmd and cmd != 'exit' and cmd != 'EXIT':
            if not authorized:
                response = establish_session(session, token)

                if response is not None:
                    client_id = response
                    authorized = True
                else:
                    print("Invalid token. lease obtain new token")
                    token = get_oauth_token()

            if authorized:
                response = message_parser(cmd, session, token, client_id)
                if response == "UNKNOWN COMMAND":
                    print(response)
                    print("WRITE HELP, COMMAND OR COMMANDS TO LIST ALL COMMANDS")
                elif response == "HELP":
                    help_print()
                else:
                    parser_res = response_parser(response)
                    if parser_res is None:
                        authorized = False

        elif cmd == 'exit' or cmd == 'EXIT':
            stop = True


def token_response(response):
    json_response = response.json()

    if response.ok:
        items = json_response["items"][0]
        return items["data"]["id"]

    return None


def response_parser(response):
    """
    Verifica a mensagem do servidor e apresenta-a ao cliente.
    """
    print("Status Code: {}".format(response.status_code))
    try:
        json_response = response.json()
    except ValueError:
        json_response = {"items": [{}]}
    if response.ok:
        items = json_response["items"][0]
        if 'href' in items:
            print("URI: {}".format(items["href"]))
        elif 'data' in items:
            if items["data"]:
                for data_line in items["data"]:
                    data_line = map(lambda x: str(x), data_line)
                    print("Data: {}".format(", ".join(data_line)))
            else:
                print("Data: []")
    if "title" in json_response:
        print("Title: {}".format(json_response["title"]))
        if json_response["title"] == "Invalid Authorization Code":
            return None
    
    return True


def help_print():
    """
    Print um menu de comandos disponiveis na plataforma.
    """
    print("------- LIST OF COMMANDS -------")
    print('MIND THE QUOTES')
    print('------- ADD COMMANDS -------')
    print('ADD USER "NAME" "USERNAME" PASSWORD')
    print('ADD SERIE NAME YYYY-MM-DD "SYNOPSIS" CATEGORY_ID')
    print('ADD EPISODIO "NAME" "DESCRIPTION" SERIE_ID')
    print("ADD USER_ID SERIE_ID CLASSIFICATION_INITIALS")
    print('------- SHOW & REMOVE COMMANDS -------')
    print("SHOW/REMOVE USER USER_ID")
    print("SHOW/REMOVE SERIE SERIE_ID")
    print("SHOW/REMOVE EPISODIO EPISODIO_ID")
    print("SHOW/REMOVE ALL USERS/SERIE/EPISODIO")
    print("SHOW/REMOVE ALL SERIE_U USER_ID")
    print("SHOW/REMOVE ALL SERIE_C CATEGORY_ID")
    print("SHOW/REMOVE ALL EPISODIO SERIE_ID")
    print("------- UPDATE COMMANDS -------")
    print("UPDATE SERIE USER_ID SERIE_ID CLASSIFICATION_ID")
    print("UPDATE USER USER_ID PASSWORD")
    print("exit or EXIT to exit out of the CLI")


def message_parser(message, session, token, client_id):
    """
    Verifica a mensagem recebida e interpreta-a.
    """

    ret = "UNKNOWN COMMAND"
    elements = message.split()

    if re.match(r"ADD USER \"[ A-Za-z]{1,128}\" \"[ A-Za-z\d]{1,64}\" [ A-Za-z\d]{1,64}", message):
        name, username, password = re.findall(
            r"ADD USER (\"[ A-Za-z]{1,128}\") (\"[ A-Za-z\d]{1,64}\") ([ A-Za-z\d]{1,64})", message)[0]
        return session.post("https://localhost:5000/utilizadores", data=json.dumps({"name": name.strip('"'), "username": username.strip('"'), "password": password, "token": token, "client_id": client_id}))
    elif re.match(r"ADD SERIE [ A-Za-z\-,.\d]{1,20} [\d]{4}-[\d]{2}-[\d]{2} \"[ A-Za-z\-,.\d]+\" \d+", message):
        name, date, synopse, category_id = re.findall(
            r"ADD SERIE ([ A-Za-z\-,.\d]{1,20}) ([\d]{4}-[\d]{2}-[\d]{2}) (\"[ A-Za-z\-,.\d]+\") (\d+)", message)[0]
        return session.post("https://localhost:5000/series", data=json.dumps({"name": name, "start_date": date, "synopse": synopse.strip('"'), "category_id": int(category_id), "token": token, "client_id": client_id}))
    elif re.match(r"ADD EPISODIO \"[ A-Za-z\d,.']+\" \"[ A-Za-z\d,.']+\" \d+", message):
        name, description, serie_id = re.findall(
            r"ADD EPISODIO (\"[ A-Za-z\d,.\-']+\") (\"[ A-Za-z\d,.\-']+\") (\d+)", message)[0]
        return session.post('https://localhost:5000/episodios', data=json.dumps({"name": name.strip('"'), "description": description.strip('"'), "serie_id": int(serie_id), "token": token, "client_id": client_id}))
    elif re.match(r"ADD \d+ \d+ [M|MM|S|B|MB]", message):
        return session.post('https://localhost:5000/series/' + elements[2], data=json.dumps({"user_id": int(elements[1]), "classification": elements[3], "token": token, "client_id": client_id}))

    elif re.match(r"REMOVE USER \d+", message):
        return session.delete('https://localhost:5000/utilizadores/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"REMOVE SERIE \d+", message):
        return session.delete('https://localhost:5000/series/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"REMOVE EPISODIO \d+", message):
        return session.delete('https://localhost:5000/episodios/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL USERS", message):
        return session.delete('https://localhost:5000/utilizadores', data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL SERIE_U \d+", message):
        return session.delete('https://localhost:5000/series', data=json.dumps({"op": elements[2], "user_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL SERIE_C \d+", message):
        return session.delete('https://localhost:5000/series', data=json.dumps({"op": elements[2], "category_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL SERIE", message):
        return session.delete('https://localhost:5000/series', data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL EPISODIO \d+", message):
        return session.delete('https://localhost:5000/episodios', data=json.dumps({"op": elements[2], "serie_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"REMOVE ALL EPISODIO", message):
        return session.delete('https://localhost:5000/episodios', data=json.dumps({"token": token, "client_id": client_id}))

    elif re.match(r"SHOW USER \d+", message):
        return session.get('https://localhost:5000/utilizadores/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"SHOW SERIE \d+", message):
        return session.get('https://localhost:5000/series/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"SHOW EPISODIO \d+", message):
        return session.get('https://localhost:5000/episodios/' + elements[2], data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL USERS", message):
        return session.get('https://localhost:5000/utilizadores', data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL SERIE_U \d+", message):
        return session.get('https://localhost:5000/series', data=json.dumps({"op": elements[2], "user_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL SERIE_C \d+", message):
        return session.get('https://localhost:5000/series', data=json.dumps({"op": elements[2], "category_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL SERIE", message):
        return session.get('https://localhost:5000/series', data=json.dumps({"token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL EPISODIO \d+", message):
        return session.get('https://localhost:5000/episodios', data=json.dumps({"op": elements[2], "serie_id": int(elements[3]), "token": token, "client_id": client_id}))
    elif re.match(r"SHOW ALL EPISODIO", message):
        return session.get('https://localhost:5000/episodios', data=json.dumps({"token": token, "client_id": client_id}))

    elif re.match(r"UPDATE SERIE \d+ \d+ [M|MM|S|B|MB]", message):
        return session.patch('https://localhost:5000/series/' + elements[3], data=json.dumps({"user_id": int(elements[2]), "classification": elements[4], "token": token, "client_id": client_id}))
    elif re.match(r"UPDATE USER \d+ [A-Za-z\d]+", message):
        return session.patch('https://localhost:5000/utilizadores/' + elements[2], data=json.dumps({"password": elements[3], "token": token, "client_id": client_id}))

    elif re.match(r"^HELP|COMMANDS|COMMAND|help|commands|command$", message):
        return "HELP"

    return ret


if __name__ == "__main__":
    handle_requests()
