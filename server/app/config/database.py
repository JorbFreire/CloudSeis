from typing import Literal
from os import path, getcwd, getenv
from ._checkForEnvValue import checkForEnvValue

database_root_path = path.join(getcwd(), 'app/database')
migrations_root_path = path.join(database_root_path, 'migrations')

modeKeyType = Literal["production", "development", "test"]

dbConfigOptions = {
    "production": {
        "dbname": getenv("DATABASE_NAME"),
        "user": getenv("DATABASE_USER"),
        "password": getenv("DATABASE_PASSWORD"),
        "host": getenv("DATABASE_HOST"),
        "port": getenv("DATABASE_PORT")
    },
    "development": {
        "dbname": checkForEnvValue("DATABASE_NAME", "admin"),
        "user": checkForEnvValue("DATABASE_USER", "admin"),
        "password": checkForEnvValue("DATABASE_PASSWORD", "mysecretpassword"),
        "host": checkForEnvValue("DATABASE_HOST", "localhost"),
        "port": checkForEnvValue("DATABASE_PORT", "5432")
    },
    # *** test connections blocked by white list
    "test": {
        "dbname": checkForEnvValue("DATABASE_NAME", "admin"),
        "user": checkForEnvValue("DATABASE_USER", "admin"),
        "password": checkForEnvValue("DATABASE_PASSWORD", "mysecretpassword"),
        "host": checkForEnvValue("DATABASE_HOST", "localhost"),
        "port": checkForEnvValue("DATABASE_PORT", "5432")
    }
}


def get_db_uri(mode: modeKeyType):
    dbConfig = dbConfigOptions[mode]
    dbConfigString = f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}"
    if "port" in dbConfig:
        dbConfigString = f"{dbConfigString}:{dbConfig['port']}"
    dbConfigString = f"{dbConfigString}/{dbConfig['dbname']}"
    return dbConfigString
