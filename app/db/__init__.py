import os.path

from flask import Blueprint, cli
from flask_sqlalchemy import SQLAlchemy

from app import config

db = SQLAlchemy()

database = Blueprint('database', __name__,)

@database.cli.command('create')
def init_db():
    db.create_all()

@database.before_app_first_request
def create_db_file_if_does_not_exist():
    root = config.Config.BASE_DIR
    db_dir = root.join('../database')
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db.create_all()
