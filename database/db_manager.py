import psycopg2

class DbManager:
    def __init__(self):
        self.DB_CONFIG = {
            "host": "localhost",
            "user": "postgres",
            "password": "1234",
            "database": "educore_db",
            "port": "5432",
            "client_encoding": "UTF8"
        }

    def connect_bd(self):
        try:
            conn = psycopg2.connect(**self.DB_CONFIG)
            return conn
        except Exception as e:
            print(f"Ошибка подключения базы данных {e}")

    def authenticate_user(self, username, password):
        conn = self.connect_bd()

        if not conn:
            print("Ошибка подключения БД")
            return None

        cursor = conn.cursor()

        try:
            query = """
                       SELECT id, role, 
                              pgp_sym_decrypt(encrypted_password, 'my_secret_key') AS decrypted_password
                       FROM SystemUsers
                       WHERE username = %s
                       """
            cursor.execute(query, (username,))

            user = cursor.fetchone()

            if user[2] == password:
                print("Успешная авторизация")
                return user[1] # role
            else:
                print(f"Неверное имя пользователя или пароль")
                return None
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
        finally:
            cursor.close()
            conn.close()

db_manager = DbManager()




