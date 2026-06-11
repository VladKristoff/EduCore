import psycopg2

class DbManager:
    def __init__(self):
        self.conn = {
            "host": "localhost",
            "user": "postgres",
            "password": "1234",
            "database": "educore_db",
            "port": "5432",
        }