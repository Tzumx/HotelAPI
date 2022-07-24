'''Config file for tests'''
from starlette.config import environ
environ['TESTING'] = 'True' # set test_database as active

from db import TEST_DB_URL
from main import app
import pytest
from starlette.testclient import TestClient
from alembic.config import Config
from alembic import command
import os
from sqlalchemy import create_engine, MetaData


@pytest.fixture(scope='module')
def setup_db():
    """Fixture. Here we prepare DB for test purposes, yield test client
    for requests and finally - cleaning up."""
    try:
        engine_test = create_engine(TEST_DB_URL)
        meta = MetaData(engine_test)
        meta.reflect()
        meta.drop_all()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        # loading alembic config
        alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))
        alembic_cfg.set_main_option('sqlalchemy.url', TEST_DB_URL)
        command.upgrade(alembic_cfg, 'head')  # perform migrations
        yield TEST_DB_URL
    finally:
        meta.reflect()
        meta.drop_all()
        engine_test.dispose()


@pytest.fixture()
def client(setup_db):
    with TestClient(app) as client:
        yield client
