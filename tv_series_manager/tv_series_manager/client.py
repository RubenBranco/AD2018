# -*- coding:utf-8 -*-
from __future__ import print_function
import requests
import re
import json
import os


def handle_requests():

    session = requests.Session()
    session.cert = [os.path.join("..", "client.crt"), os.path.join("..", "client.key")]
    session.verify = os.path.join("..", "root.pem")
    stop = False
    while not stop:
        cmd = raw_input("Comando? ")
        if cmd and cmd != 'exit' and cmd != 'EXIT':
            response = message_parser(cmd, session)
            if response == "UNKNOWN COMMAND":
                print(response)
                print("WRITE HELP, COMMAND OR COMMANDS TO LIST ALL COMMANDS")
            elif response == "HELP":
                help_print()
            else:
                response_parser(response)
        elif cmd == 'exit' or cmd == 'EXIT':
            stop = True


def response_parser(response):
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


def help_print():
    print("------- LIST OF COMMANDS -------")
    print('MIND THE QUOTES')
    print('------- ADD COMMANDS -------')
    print('ADD USER "NAME" "USERNAME" PASSWORD')
    print('ADD SERIE NAME YYYY-MM-DD "SYNOPSIS" CATEGORY_ID')
    print('ADD EPISODIO "NAME" "DESCRIPTION" SERIE_ID')
    print("USER_ID SERIE_ID CLASSIFICATION_INITIALS")
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


def message_parser(message, session):
    """
    Verifica a mensagem recebida e interpreta-a
    """

    ret = "UNKNOWN COMMAND"
    elements = message.split()

    if re.match(r"ADD USER \"[ A-Za-z]{1,128}\" \"[ A-Za-z\d]{1,64}\" [ A-Za-z\d]{1,64}", message):
        name, username, password = re.findall(
            r"ADD USER (\"[ A-Za-z]{1,128}\") (\"[ A-Za-z\d]{1,64}\") ([ A-Za-z\d]{1,64})", message)[0]
        return session.post("https://localhost:5000/utilizadores", data=json.dumps({"name": name.strip('"'), "username": username.strip('"'), "password": password}))
    elif re.match(r"ADD SERIE [ A-Za-z\-,.\d]{1,20} [\d]{4}-[\d]{2}-[\d]{2} \"[ A-Za-z\-,.\d]+\" \d+", message):
        name, date, synopse, category_id = re.findall(
            r"ADD SERIE ([ A-Za-z\-,.\d]{1,20}) ([\d]{4}-[\d]{2}-[\d]{2}) (\"[ A-Za-z\-,.\d]+\") (\d+)", message)[0]
        return session.post("https://localhost:5000/series", data=json.dumps({"name": name, "start_date": date, "synopse": synopse.strip('"'), "category_id": int(category_id)}))
    elif re.match(r"ADD EPISODIO \"[ A-Za-z\d,.']+\" \"[ A-Za-z\d,.']+\" \d+", message):
        name, description, serie_id = re.findall(
            r"ADD EPISODIO (\"[ A-Za-z\d,.\-']+\") (\"[ A-Za-z\d,.\-']+\") (\d+)", message)[0]
        return session.post('https://localhost:5000/episodios', data=json.dumps({"name": name.strip('"'), "description": description.strip('"'), "serie_id": int(serie_id)}))
    elif re.match(r"ADD \d+ \d+ [M|MM|S|B|MB]", message):
        return session.post('https://localhost:5000/series/' + elements[2], data=json.dumps({"user_id": int(elements[1]), "classification": elements[3]}))

    elif re.match(r"REMOVE USER \d+", message):
        return session.delete('https://localhost:5000/utilizadores/' + elements[2])
    elif re.match(r"REMOVE SERIE \d+", message):
        return session.delete('https://localhost:5000/series/' + elements[2])
    elif re.match(r"REMOVE EPISODIO \d+", message):
        return session.delete('https://localhost:5000/episodios/' + elements[2])
    elif re.match(r"REMOVE ALL USERS", message):
        return session.delete('https://localhost:5000/utilizadores')
    elif re.match(r"REMOVE ALL SERIE_U \d+", message):
        return session.delete('https://localhost:5000/series', data=json.dumps({"op": elements[2], "user_id": int(elements[3])}))
    elif re.match(r"REMOVE ALL SERIE_C \d+", message):
        return session.delete('https://localhost:5000/series', data=json.dumps({"op": elements[2], "category_id": int(elements[3])}))
    elif re.match(r"REMOVE ALL SERIE", message):
        return session.delete('https://localhost:5000/series')
    elif re.match(r"REMOVE ALL EPISODIO \d+", message):
        return session.delete('https://localhost:5000/episodios', data=json.dumps({"op": elements[2], "serie_id": int(elements[3])}))
    elif re.match(r"REMOVE ALL EPISODIO", message):
        return session.delete('https://localhost:5000/episodios')

    elif re.match(r"SHOW USER \d+", message):
        return session.get('https://localhost:5000/utilizadores/' + elements[2])
    elif re.match(r"SHOW SERIE \d+", message):
        return session.get('https://localhost:5000/series/' + elements[2])
    elif re.match(r"SHOW EPISODIO \d+", message):
        return session.get('https://localhost:5000/episodios/' + elements[2])
    elif re.match(r"SHOW ALL USERS", message):
        return session.get('https://localhost:5000/utilizadores')
    elif re.match(r"SHOW ALL SERIE_U \d+", message):
        return session.get('https://localhost:5000/series', data=json.dumps({"op": elements[2], "user_id": int(elements[3])}))
    elif re.match(r"SHOW ALL SERIE_C \d+", message):
        return session.get('https://localhost:5000/series', data=json.dumps({"op": elements[2], "category_id": int(elements[3])}))
    elif re.match(r"SHOW ALL SERIE", message):
        return session.get('https://localhost:5000/series')
    elif re.match(r"SHOW ALL EPISODIO \d+", message):
        return session.get('https://localhost:5000/episodios', data=json.dumps({"op": elements[2], "serie_id": int(elements[3])}))
    elif re.match(r"SHOW ALL EPISODIO", message):
        return session.get('https://localhost:5000/episodios')

    elif re.match(r"UPDATE SERIE \d+ \d+ [M|MM|S|B|MB]", message):
        return session.patch('https://localhost:5000/series/' + elements[3], data=json.dumps({"user_id": int(elements[2]), "classification": elements[4]}))
    elif re.match(r"UPDATE USER \d+ [A-Za-z\d]+", message):
        return session.patch('https://localhost:5000/utilizadores/' + elements[2], data=json.dumps({"password": elements[3]}))

    elif re.match(r"^HELP|COMMANDS|COMMAND|help|commands|command$", message):
        return "HELP"

    return ret


if __name__ == "__main__":
    handle_requests()
