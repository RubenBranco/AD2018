#imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


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

def conecta_db():
    """
    Conecta-se a base de dados, ou inicializa-a
    com base no ficheiro schema.sql
    """
    db_created = os.path.isfile(app.config['DATABASE'])
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    if not db_created:
        with app.open_resource(schema.sql, mode='r') as f:
            conn.cursor.execute(f.read())
        db.commit()
    return conn

def get_db():
    """
    Abre uma nova conexão à base de dados se ainda não houver
    para o contexto corrente da aplicacao
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = conecta_db()
    return g.sqlite_db

@app.teardown_appcontext
def fecha_db(error):
    """Com o fim do request fecha a base de dados"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
@app.route('/utilizadores')
# TODO definir metodos permitidos
def users():
    pass
@app.route('/series')
# TODO definir metodos permitidos
def series():
    pass
@app.route('/episodios')
# TODO definir metodos permitidos
def episodios():
    pass

if __name__ == "__main__":
    app.run()