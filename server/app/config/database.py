from typing import Literal
from os import path, getcwd

database_root_path = path.join(getcwd(), 'app/database')
migrations_root_path = path.join(database_root_path, 'migrations')

modeKeyType = Literal["production", "development", "test"]

dbConfigOptions = {
    "production": {
        "dbname": "admin",
        "user": "admin",
        "password": "mysecretpassword",
        "host": "localhost",
        "port": "5432"
    },
    "development": {
        "dbname": "admin",
        "user": "admin",
        "password": "mysecretpassword",
        "host": "localhost",
        "port": "5432"
    },
    "test": {
        "dbname": "admin",
        "user": "admin",
        "password": "mysecretpassword",
        "host": "localhost",
        "port": "5432"
    }
}


def get_db_uri(mode: modeKeyType):
    dbConfig = dbConfigOptions[mode]
    return f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}:{dbConfig['port']}/{dbConfig['dbname']}"
