import sqlite3
from sqlite3 import Error
import time

def create_connection(path): #https://realpython.com/python-sql-libraries/#sqlite
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def is_slime_word(guild,word): #fixme maybe has slime words and check for all of them
    submitter_id, time = get_slime_word_data(guild,word)
    activator_id = get_slime_word_activator_id(guild,word)
    return submitter_id is not None and activator_id is None


def add_words(word_list, author, guild):
    sql_connection = create_connection('test.db')
    insert_time = time.strftime('%Y-%m-%d %H:%M:%S')
    for word in word_list:
        print(f'insert into slime_words (GUILD_ID, TRIGGER_WORD, SUBMITTER_USER_ID, SUBMITTER_USERNAME, SUBMISSION_TIME) values ( {guild.id},"{word}",{author.id},"{author.display_name}","{insert_time}")')
        sql_connection.execute(f'insert into slime_words (GUILD_ID, TRIGGER_WORD, SUBMITTER_USER_ID, SUBMITTER_USERNAME, SUBMISSION_TIME) values ( {guild.id},"{word}",{author.id},"{author.display_name}","{insert_time}")')
    sql_connection.commit()


def disallow_words(word_list, author, guild):
    sql_connection = create_connection('test.db')
    insert_time = time.strftime('%Y-%m-%d %H:%M:%S')

    for word in word_list:
        sql_connection.execute(
            f'insert into slime_words (GUILD_ID, DISSALLOWED_WORD, SUBMITTER_USER_ID, SUBMITTER_USERNAME, SUBMISSION_TIME) values ( {guild.id},"{word}",{author.id},"{author.display_name}","{insert_time}")')
    sql_connection.commit()

def get_slime_word_data(guild,word):
    sql_connection = create_connection('test.db')
    cursor = sql_connection.execute(f"select * from slime_words where GUILD_ID = {guild.id} and TRIGGER_WORD = '{word}'")
    result = cursor.fetchone()
    if result is None:
        return None, None
    return result[3], result[5] #submitter_ID submition_time

def get_slime_word_activator_id(guild,word):
    sql_connection = create_connection('test.db')
    cursor = sql_connection.execute(f"select ACTIVATOR_USER_ID from slime_words where GUILD_ID = {guild.id} and TRIGGER_WORD = '{word}'")
    result = cursor.fetchone()
    if result is None:
        return None,
    return result[0]


#slime keys: incrementor unique key, server or guild, trigger_word, submitter_user_id, submitter username (as a backup), submission_time,  activator_user_id, activation_time

#blacklist keys incrementor unique key, server or guild, trigger_word, submitter_user_id, submitter username (as a backup), submission_time,

def remove_word(guild,word, activator):
    sql_connection = create_connection('test.db')

    activation_time = time.strftime('%Y-%m-%d %H:%M:%S')
    sql_connection.execute(f'update slime_words set ACTIVATOR_USER_ID={activator.id} , ACTIVATOR_USERNAME="{activator.name}",ACTIVATION_TIME="{activation_time}" where GUILD_ID = {guild.id} and TRIGGER_WORD = "{word}"')
    sql_connection.commit()

sql_connection = create_connection("./test.db")
print("connected to database")
#sql_connection.execute("SELECT word FROM words")
sql_connection.execute("drop table if exists slime_words")
sql_connection.execute("drop table if exists disallowed_words")
sql_connection.execute("CREATE TABLE slime_words (PK INTEGER PRIMARY KEY AUTOINCREMENT, GUILD_ID BIGINT NOT NULL , TRIGGER_WORD VARCHAR(200) NOT NULL, SUBMITTER_USER_ID BIGINT NOT NULL, SUBMITTER_USERNAME VARCHAR(200) NOT NULL,SUBMISSION_TIME DATETIME NOT NULL, ACTIVATOR_USER_ID BIGINT , ACTIVATOR_USERNAME VARCHAR(200),ACTIVATION_TIME DATETIME)")
sql_connection.execute("CREATE TABLE disallowed_words (PK INTEGER PRIMARY KEY  AUTOINCREMENT, GUILD_ID BIGINT NOT NULL , DISALLOWED_WORD VARCHAR(200) NOT NULL, SUBMITTER_USER_ID BIGINT NOT NULL, SUBMITTER_USERNAME VARCHAR(200) NOT NULL,SUBMISSION_TIME DATETIME NOT NULL )")
#sql_connection.commit()
#get_slime_word_data(guild=1,word='test1')