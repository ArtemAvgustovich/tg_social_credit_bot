import os
import psycopg2

# DB settings and commands
DATABASE_URL = os.getenv('DATABASE_URL')
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS social_credit (
user_id integer(64),
chat_id integer(64),
rating integer(16),
PRIMARY KEY (user_id, chat_id)
);
"""
CHANGE_RATING = """
INSERT INTO social_credit (user_id, chat_id, rating)
VALUES ({user_id}, {chat_id}, {rating})
"""
SELECT_RATING = """
SELECT rating
FROM social_credit
WHERE user_id={user_id} AND chat_id={chat_id}
"""
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()


def setup_table():
    cursor.execute(CREATE_TABLE)
    connection.commit()


def change_rating(user_id, chat_id, delta):
    cursor.execute(SELECT_RATING.format(user_id=user_id, chat_id=chat_id))
    print(cursor.fetchall())
    rating = cursor.fetchone()
    print(rating)
    if rating is None:
        rating = 0
    cursor.execute(CHANGE_RATING.format(user_id=user_id, chat_id=chat_id, rating=rating+delta))
    connection.commit()
