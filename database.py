import os
import psycopg2

# DB settings and commands
DATABASE_URL = os.getenv('DATABASE_URL')
CREATE_TABLE = """
               CREATE TABLE IF NOT EXISTS social_credit (
               user_id integer,
               chat_id integer,
               rating integer,
               PRIMARY KEY (user_id, chat_id)
               );
               """

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()


def setup_table():
    cursor.execute(CREATE_TABLE)
