# -*- coding:utf-8 -*-
#imports
from __future__ import print_function
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
import sys
import json


app = Flask(__name__) # cria instancia da aplicacao
app.config.from_object(__name__) # carrega o ficheiro de config deste ficheiro , series_manager.py

# Carrega a config default e faz override a config de uma environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'series_manager.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """
    Conecta-se a base de dados, ou inicializa-a
    com base no ficheiro schema.sql
    """
    db_created = os.path.isfile(app.config['DATABASE'])
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    if not db_created:
        with app.open_resource("schema.sql", mode='r') as f:
            conn.cursor().executescript(f.read())
        with app.open_resource("inserts.sql", "r") as f:
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
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def fecha_db(error):
    """Com o fim do request fecha a base de dados"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
@app.route('/utilizadores', methods=["POST", "GET"])
@app.route('/utilizadores/<int:id>', methods=["GET", "PATCH"])
def users(id=None):
    res = ''
    if request.method == "GET":
        if id is not None:
            query = "SELECT * FROM users WHERE id=?"
            res = {"items": [{"data": query_db(query, [id])}]}
        else:
            query = "SELECT * FROM users"
            res = {"items": [{"data": query_db(query)}]}
    elif request.method == "POST":
        data = json.loads(request.data)
        query = "INSERT INTO users VALUES (?,?,?,?)"
        idnum = query_db("SELECT id FROM users WHERE id=(SELECT MAX(id) FROM users)", one=True)
        if not idnum:
            idnum = 0
        query_db(query, [idnum, data["name"], data["username"], data["password"]])
        res = {"items": [{"href": "/utilizadores/{}".format(idnum)}]}
    elif request.method == "PATCH":
        data = json.loads(request.data)
        query_update = "UPDATE users SET password=? WHERE id=?"
        query_select = "SELECT * FROM users WHERE id=?"
        query_db(query_update, [data["id"], data["password"]])
        new_line = query_db(query_select, [data["id"]], one=True)
        res = {"items": [{"data": new_line}]}
    return make_response(json.dumps(res))

@app.route('/series', methods=["POST", "GET"])
@app.route('/series/<int:id>', methods=["GET", "PUT"])
def series(id=None):
    res = ''
    if request.method == "POST":
        data = json.loads(request.data)
        idnum = query_db("SELECT id FROM serie WHERE id=(SELECT MAX(id) FROM serie)")
        if not idnum:
            idnum = 0
        query = "INSERT into serie VALUES (?, ?, ?, ?, ?)"
        category_id = query_db("SELECT id from category WHERE name=?", [data["category"]], one=True)
        query_db(query, [idnum, data["name"], data["start_date"], data["synopse"], category_id])
        res = {"items": [{"href": "/series/{}".format(idnum)}]}
    if request.method == "GET":
        if id is None:
            query = "SELECT * FROM serie"
            res = {"items": [{"data": query_db(query)}]}
    
    return make_response(json.dumps(res))

@app.route('/episodios', methods=["POST", "GET"])
@app.route('/series/<int:id>', methods=["GET", "PUT"])
def episodios(id=None):
    res = ''
    if request.method == "POST":
        data = json.loads(request.data)
        idnum = query_db("SELECT id FROM episode WHERE id=(SELECT MAX(id) FROM episode)", one=True)
        if not idnum:
            idnum = 0
        query = "INSERT into episode VALUES (?, ?, ?, ?)"
        query_db(query, [idnum, data["name"], data["description"], data["serie_id"]])
        res = {"items": [{"href": "/episodios/{}".format(idnum)}]}
    return make_response(json.dumps(res))

if __name__ == "__main__":
    app.run()