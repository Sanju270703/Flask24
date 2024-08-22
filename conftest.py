# conftest.py
# import pytest
# from app import app, db, mqtt_client
# from test_config import TestConfig

# @pytest.fixture(scope='module')
# def test_client():
#     app.config.from_object(TestConfig)

#     with app.test_client() as testing_client:
#         with app.app_context():
#             db.create_all()
#             yield testing_client
#             db.drop_all()

# @pytest.fixture(scope='function')
# def init_database():
#     db.create_all()
#     yield db
#     db.session.remove()
#     db.drop_all()

# @pytest.fixture
# def mock_mqtt_client(mocker):
#     mocker.patch.object(mqtt_client, 'publish')
#     return mqtt_client


# import sys
# import os
# # Add the path to the directory containing 'source' module
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest, unittest
from app import app, db, mqtt_client, Todo, on_message, on_connect, publish
from pytest_mock_resources import create_mysql_fixture
from test_config import TestConfig
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
from member import Employee
import pymysql

pymysql.install_as_MySQLdb()

Base = declarative_base()
mysql = create_mysql_fixture(Base, session=True)


@pytest.fixture(scope='session')
def mysql_engine():
    engine = create_engine('sqlite:///:memory:')
    return engine

@pytest.fixture(scope='session')
def mysql_session(mysql_engine):
    Session = sessionmaker(bind=mysql_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='session')
def init_database(mysql_session):
    db.metadata.create_all(bind=mysql_session.bind)
    yield
    db.session.remove()
    db.metadata.drop_all(bind=mysql_session.bind)

@pytest.fixture(scope='package')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# @pytest.fixture
# def new_emp():
#     return Employee(emp_id = 1, emp_name = "alice")



@pytest.fixture
def mock_mqtt_client(mocker):
    mqtt_client = mocker.patch('app.mqtt_client', autospec=True)
    # mqtt_client = MagicMock()

    mqtt_client.publish = MagicMock()
    return mqtt_client


