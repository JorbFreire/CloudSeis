from os import path, getcwd

database_root_path = path.join(getcwd(), 'app/database')
migrations_root_path = path.join(database_root_path, 'migrations')

dbConfig = {
	"dbname": "admin",
	"user": "admin",
	"password": "mysecretpassword",
	"host": "localhost",
	"port": "5432"
}

db_uri = f"postgresql://{dbConfig['user']}:${dbConfig['password']}@{dbConfig['host']}:{dbConfig['port']}/{dbConfig['dbname']}"
