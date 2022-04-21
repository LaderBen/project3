"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name

import pytest
from app import create_app
from app.db import db


@pytest.fixture()
def application():
    """This makes the app"""
    application = create_app()
    application.config.update(
    #     {
    #     "TESTING": True,
    # }
        ENV = 'development',
    )
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        # drops the database tables after the test runs
        # db.drop_all()
    # yield application



@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()
