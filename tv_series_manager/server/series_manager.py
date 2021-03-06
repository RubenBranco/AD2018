# -*- coding:utf-8 -*-
# imports
from __future__ import print_function
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response
import sys
import json
import ssl
from requests_oauthlib import OAuth2Session


application = Flask(__name__)  # cria instancia da aplicacao
# carrega o ficheiro de config deste ficheiro , series_manager.py
application.config.from_object(__name__)

# GITHUB
client_id = 'd58498b6e10353206e26'
client_secret = 'c6a8aca3d7e69b7a69a7d90e70d259902e9a7f3d'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

tokens = {}

# Carrega a config default e faz override a config de uma environment variable
application.config.update(dict(
    DATABASE=os.path.join(application.root_path, 'series_manager.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

application.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """
    Conecta-se a base de dados, ou inicializa-a
    com base no ficheiro schema.sql
    """
    db_created = os.path.isfile(application.config['DATABASE'])
    conn = sqlite3.connect(application.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    if not db_created:
        with application.open_resource("schema.sql", mode='r') as f:
            conn.cursor().executescript(f.read())
        with application.open_resource("inserts.sql", "r") as f:
            conn.cursor().executescript(f.read())
        conn.commit()
    return conn


def get_db():
    """
    Abre uma nova conexão à base de dados se ainda não houver
    para o contexto corrente da aplicacao
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def query_db(query, args=(), one=False):
    """
    Interroga a base de dados através de queries(SELECT) dadas.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    """
    Conecta-se à base de dados e executa INSERT e UPDATE queries.
    """
    conn = get_db()
    conn.cursor().execute(query, args)
    conn.commit()


@application.teardown_appcontext
def fecha_db(error):
    """
    Com o fim do request fecha a base de dados.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def exists(query, args=()):
    """
    Verifica se uma entrada existe na base de dados.
    """
    fetch = query_db(query, args, one=True)
    if fetch is not None:
        return True
    return False


@application.route('/')
@application.route('/utilizadores', methods=["POST", "GET", "DELETE"])
@application.route('/utilizadores/<int:id>', methods=["GET", "PATCH", "DELETE"])
def users(id=None):
    """
    Recebe requests para o url /utilizadores/ e gere com a base de dados.
    """
    res = {}
    if request.data:
        data = json.loads(request.data)
    else:
        data = {}
    code = 200

    if data["client_id"] in tokens and tokens[data["client_id"]] == data["token"]:
        if request.method == "GET":
            if id is not None:
                query = "SELECT * FROM users WHERE id=?"
                user = query_db(query, [id], one=True)
                if user is None:
                    user = []
                else:
                    user = [list(user)]
                res = {"items": [{"data": user}]}
                code = (200 if user else 404)
            else:
                query = "SELECT * FROM users"
                all_users = query_db(query)
                if not all_users:
                    all_users = []
                else:
                    all_users = list(map(lambda x: list(x), all_users))
                res = {"items": [{"data": all_users}]}
        elif request.method == "POST":
            query = "INSERT INTO users VALUES (?,?,?,?)"
            is_existent = exists(
                "SELECT * FROM users WHERE username=?", [data["username"]])
            if is_existent:
                res = {"title": "The resource already exists"}
                code = 409
            else:
                idnum = query_db(
                    "SELECT id FROM users WHERE id=(SELECT MAX(id) FROM users)", one=True)
                if idnum is None:
                    idnum = 0
                else:
                    idnum = list(idnum)[0] + 1
                execute_db(query, [idnum, data["name"],
                                data["username"], data["password"]])
                res = {"items": [{"href": "/utilizadores/{}".format(idnum)}]}
                code = 201
        elif request.method == "PATCH":
            query = "UPDATE users SET password=? WHERE id=?"
            is_existent = exists("SELECT * FROM users WHERE id=?", [id])
            if is_existent:
                execute_db(query, [data["password"], id])
                new_line = list(query_db(
                    "SELECT * FROM users WHERE id=?", [id], one=True))
                res = {"items": [{"data": [new_line]}]}
            else:
                res = {"title": "The resource you wish to update does not exist."}
                code = 204
        elif request.method == "DELETE":
            if id is not None:
                query = "DELETE FROM users WHERE id=?"
                execute_db(query, [id])
            else:
                query = "DELETE FROM users"
                execute_db(query)
            res = {"items": [{"data": []}]}
            code = 204
    else:
        code = 400
        res = {"title": "Invalid Authorization Code"}

    return make_response(json.dumps(res), code)


@application.route('/series', methods=["POST", "GET", "DELETE"])
@application.route('/series/<int:id>', methods=["GET", "POST", "PATCH", "DELETE"])
def series(id=None):
    """
    Recebe requests para o url /series/ e gere com a base de dados.
    """
    res = {}
    if request.data:
        data = json.loads(request.data)
    else:
        data = {}
    code = 200
    if data["client_id"] in tokens and tokens[data["client_id"]] == data["token"]:
        if request.method == "POST":
            if id is None:
                is_existent = exists(
                    "SELECT * FROM serie WHERE name=?", [data["name"]])
                if is_existent:
                    res = {"title": "The resource already exists"}
                    code = 409
                else:
                    idnum = query_db(
                        "SELECT id FROM serie WHERE id=(SELECT MAX(id) FROM serie)", one=True)
                    if idnum is None:
                        idnum = 0
                    else:
                        idnum = list(idnum)[0] + 1
                    query = "INSERT into serie VALUES (?, ?, ?, ?, ?)"
                    execute_db(
                        query, [idnum, data["name"], data["start_date"], data["synopse"], data["category_id"]])
                    res = {"items": [{"href": "/series/{}".format(idnum)}]}
                    code = 201
            else:
                is_existent = exists(
                    "SELECT * from list_series WHERE user_id=? AND serie_id=?", [data["user_id"], id])
                if is_existent:
                    res = {"title": "The resource already exists"}
                    code = 409
                else:
                    query = "INSERT INTO list_series VALUES (?,?,?)"
                    classification_id = list(query_db("SELECT id FROM classification WHERE initials=?", [
                        data["classification"]], one=True))[0]
                    execute_db(query, [data["user_id"], classification_id, id])
                    res = {
                        "items": [{"href": "/series/{}".format(id), "op": "list_series"}]}
                    code = 201
        elif request.method == "GET":
            if id is None:
                if "op" not in data:
                    query = "SELECT * FROM serie"
                    all_series = query_db(query)
                    if not all_series:
                        all_series = []
                    else:
                        all_series = list(map(lambda x: list(x), all_series))
                    res = {"items": [{"data": all_series}]}
                else:
                    if data["op"] == "SERIE_U":
                        query = "SELECT * FROM list_series WHERE user_id=?"
                        all_serie_u = query_db(
                            query, [data["user_id"]])
                        if not all_serie_u:
                            all_serie_u = []
                        else:
                            all_serie_u = list(map(lambda x: list(x), all_serie_u))
                        res = {
                            "items": [{"data": all_serie_u}]}
                    elif data["op"] == "SERIE_C":
                        query = "SELECT * FROM serie WHERE category_id=?"
                        all_serie_c = query_db(query, [data["category_id"]])
                        if not all_serie_c:
                            all_serie_c = []
                        else:
                            all_serie_c = list(
                                map(lambda x: list(x), all_serie_c))
                        res = {
                            "items": [{"data": all_serie_c}]}
            else:
                query = "SELECT * FROM serie WHERE id=?"
                serie = query_db(query, [id], one=True)
                if serie is None:
                    serie = []
                else:
                    serie = [list(serie)]
                res = {"items": [{"data": serie}]}
                code = (200 if serie else 404)
        elif request.method == "PATCH":
            query = "UPDATE list_series SET classification_id=? WHERE user_id=? AND serie_id=?"
            is_existent = exists(
                "SELECT * FROM list_series WHERE user_id=? AND serie_id=?", [data["user_id"], id])
            if is_existent:
                query_select = "SELECT * FROM list_series WHERE user_id=? AND serie_id=?"
                classification_id = list(query_db("SELECT id FROM classification WHERE initials=?", [
                    data["classification"]], one=True))[0]
                execute_db(query, [classification_id,
                                data["user_id"], id])
                res = {
                    "items": [{"data": [list(query_db(query_select, [data["user_id"], id], one=True))]}]}
            else:
                res = {"title": "The resource you wish to update does not exist."}
                code = 204
        elif request.method == "DELETE":
            if request.data and "op" in data:
                if data["op"] == "SERIE_U":
                    query = "DELETE FROM list_series WHERE user_id=?"
                    execute_db(query, [data["user_id"]])
                elif data["op"] == "SERIE_C":
                    query = "DELETE FROM serie WHERE category_id=?"
                    execute_db(query, [data["category_id"]])
            else:
                if id is not None:
                    query = "DELETE FROM serie WHERE id=?"
                    execute_db(query, [id])
                else:
                    query = "DELETE FROM serie"
                    execute_db(query)
            res = {"items": [{"data": []}]}
            code = 204
    else:
        code = 400
        res = {"title": "Invalid Authorization Code"}

    return make_response(json.dumps(res), code)


@application.route('/episodios', methods=["POST", "GET", "DELETE"])
@application.route('/episodios/<int:id>', methods=["GET", "DELETE"])
def episodios(id=None):
    """
    Recebe requests para o url /episodios/ e gere com a base de dados.
    """
    res = {}
    if request.data:
        data = json.loads(request.data)
    else:
        data = {}
    code = 200

    if data["client_id"] in tokens and tokens[data["client_id"]] == data["token"]:
        if request.method == "POST":
            is_series_existent = exists(
                "SELECT * FROM serie WHERE id=?", [data["serie_id"]])
            is_existent = exists(
                "SELECT * FROM episode WHERE name=? AND serie_id=?", [data["name"], data["serie_id"]])
            if is_existent:
                res = {"title": "The resource already exists"}
                code = 409
            elif not is_series_existent:
                res = {"title": "The resource serie with id {} does not exist".format(
                    data["serie_id"])}
                code = 404
            else:
                idnum = query_db(
                    "SELECT id FROM episode WHERE id=(SELECT MAX(id) FROM episode)", one=True)
                if idnum is None:
                    idnum = 0
                else:
                    idnum = list(idnum)[0] + 1
                query = "INSERT into episode VALUES (?, ?, ?, ?)"
                execute_db(query, [idnum, data["name"],
                                data["description"], data["serie_id"]])
                res = {"items": [{"href": "/episodios/{}".format(idnum)}]}
                code = 201
        elif request.method == "GET":
            if id is not None:
                query_select = "SELECT * FROM episode WHERE id=?"
                episode = query_db(query_select, [id], one=True)
                if episode is None:
                    episode = []
                else:
                    episode = [list(episode)]
                res = {"items": [{"data": episode}]}
                code = (200 if episode else 404)
            else:
                if "op" not in data:
                    query = "SELECT * FROM episode"
                    all_episodes = query_db(query)
                    if not all_episodes:
                        all_episodes = []
                    else:
                        all_episodes = list(map(lambda x: list(x), all_episodes))
                    res = {"items": [{"data": all_episodes}]}
                else:
                    query = "SELECT * FROM episode WHERE serie_id=?"
                    all_episodes = query_db(query, [data["serie_id"]])
                    if all_episodes:
                        all_episodes = list(map(lambda x: list(x), all_episodes))
                    else:
                        all_episodes = []
                    res = {"items": [{"data": all_episodes}]}
        elif request.method == "DELETE":
            if request.data and "op" in data:
                query = "DELETE FROM episode WHERE serie_id=?"
                execute_db(query, [data["serie_id"]])
            else:
                if id is not None:
                    query = "DELETE FROM episode WHERE id=?"
                    execute_db(query, [id])
                else:
                    query = "DELETE FROM episode"
                    execute_db(query)
            res = {"items": [{"data": []}]}
            code = 204
    else:
        code = 400
        res = {"title": "Invalid Authorization Code"}

    return make_response(json.dumps(res), code)


@application.route('/token', methods=["POST"])
def token():
    data = json.loads(request.data)
    valid = True
    code = 201
    res = {}

    github = OAuth2Session(client_id, token=data["token"])
    git_response = github.get('https://api.github.com/user').json()

    if "message" in git_response and git_response["message"] == "Bad credentials":
        valid = False

    if valid:
        if tokens.keys():
            idnum = max(tokens.keys()) + 1
        else:
            idnum = 0
        tokens[idnum] = data["token"]
        res = {"items": [{"data": {"id": idnum}}]}
    else:
        res = {"title": "Invalid Authorization Code"}
        code = 400

    return make_response(json.dumps(res), code)


if __name__ == "__main__":
    connect_db()
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(os.path.join(
        '..', 'certs', 'server.crt'), os.path.join('..', 'certs', 'server.key'))
    context.load_verify_locations(os.path.join('..', 'certs', 'root.pem'))
    application.run(ssl_context=context, debug=True, threaded=True)
