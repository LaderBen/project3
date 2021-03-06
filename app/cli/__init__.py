import click
import os
from flask import current_app
from flask.cli import with_appcontext
from app.db import db


@click.command(name='create-db')
@with_appcontext
def create_database():
    root = current_app.config['BASE_DIR']
    db_dir = os.path.join(root,'../database')
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db.create_all()

@click.command(name='create-log-folder')
@with_appcontext
def create_log_folder():
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    logdir = os.path.join(root, '../logs')
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)

