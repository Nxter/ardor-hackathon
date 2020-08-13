# -*- coding: UTF-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField, CharField, TextField, IntegerField, UUIDField, BooleanField, DoubleField
from playhouse.migrate import *
from playhouse.db_url import connect
from os import environ

import warnings

warnings.filterwarnings("ignore")

MYSQL_DATABASE = environ.get("MYSQL_DATABASE", None)
MYSQL_HOSTNAME = environ.get("MYSQL_HOSTNAME", None)
MYSQL_PORT = environ.get("MYSQL_PORT", 3306)
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD", None)

if MYSQL_DATABASE is not None:
    db = MySQLDatabase(MYSQL_DATABASE, user=MYSQL_DATABASE, password=MYSQL_PASSWORD, host=MYSQL_HOSTNAME, port=int(MYSQL_PORT))
else:
    db = connect("sqlite:///sigbro_acl.db")

db.close()

class BaseModel(Model):
    class Meta:
        database = db


class acl_scanner(BaseModel):
    """Table for store scanner metadata."""
    network = CharField(max_length=10, null=False, index=True, unique=True)  # metric name
    block = IntegerField(null=True, default=1)

class acl_accounts(BaseModel):
    """Table with list of accounts"""
    network = CharField(max_length=10, null=False, index=True)  # testnet, mainnet
    timestamp = BigIntegerField(null=False)  # when access was granted
    accountRS = CharField(max_length=30, null=False, index=False)
    status = CharField(max_length=10, null=False, index=False) # member, silver, gold
    
acl_accounts.add_index(acl_accounts.network, acl_accounts.accountRS, unique=True)

def init_db():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        db.connect()
        db.create_tables(
            [
                acl_scanner,
                acl_accounts,
            ]
        )
        db.close()

