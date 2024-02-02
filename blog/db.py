# SQL database set up file

import sqlite3
import click

from flask import current_app, g

def get_db():
    if 'database_connection' not in g:
        g.database_connection = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.database_connection.row_factory = sqlite3.Row

    return g.database_connection     

def close_db(e=None):
    db = g.pop('database_connection', None)

    if db is not None:
        db.close()

# create the tables
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialised the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
