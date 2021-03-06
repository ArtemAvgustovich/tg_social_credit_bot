import os
import psycopg2

# DB settings and commands
DATABASE_URL = os.getenv('DATABASE_URL')
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS social_credit (
user_id BIGINT NOT NULL,
chat_id BIGINT NOT NULL,
username VARCHAR,
rating INTEGER,
PRIMARY KEY (user_id, chat_id)
);
"""
ADD_USER_RATING = """
INSERT INTO social_credit (user_id, chat_id, username, rating)
VALUES ({user_id}, {chat_id}, '{username}', {rating})
"""
SELECT_RATING = """
SELECT rating
FROM social_credit
WHERE user_id={user_id} AND chat_id={chat_id}
"""
CHANGE_RATING = """
UPDATE social_credit
SET rating = {rating}
WHERE user_id={user_id} AND chat_id={chat_id}
"""
SHOW_STATS = """
SELECT username, rating
FROM social_credit
WHERE chat_id={chat_id}
"""
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()


def setup_table():
    cursor.execute(CREATE_TABLE)
    connection.commit()


def change_rating(user_id, chat_id, username, delta):
    cursor.execute(SELECT_RATING.format(user_id=user_id, chat_id=chat_id))
    data = cursor.fetchone()
    if data is None:
        new_rating = delta
        cursor.execute(ADD_USER_RATING.format(user_id=user_id, chat_id=chat_id, username=username, rating=new_rating))
    else:
        new_rating = data[0]+delta
        cursor.execute(CHANGE_RATING.format(user_id=user_id, chat_id=chat_id, rating=new_rating))
    connection.commit()
    return new_rating


def chat_stats(chat_id):
    cursor.execute(SHOW_STATS.format(chat_id=chat_id))
    return cursor.fetchall()
