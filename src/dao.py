import psycopg2
from collections import defaultdict


def connect():
    return psycopg2.connect(user = "postgres", password = "",
                host = "emoji.cqppiab1dnlz.eu-central-1.rds.amazonaws.com",
                port = 5432, database = "emoji_database")

   
def get_word_count():
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('''select sum(w.count) from words w''')
        return cursor.fetchone()[0]
    except Exception as error:
        print(error)
    finally:
        if(connection):
            cursor.close()
            print("closed")

def get_emoji_count():
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('''select sum(e.count) from emojis e''')
        return cursor.fetchone()[0]
    except Exception as error:
        print(error)
    finally:
        if(connection):
            cursor.close()
            print("closed")

def _format_result(result):
      
    emojis = defaultdict()
    words = defaultdict()
    word_emoji = defaultdict(list)

    for (word, emoji, w_count, e_count, w_e_count) in result:
            words[word] = w_count
            emojis[emoji] = e_count

            if word_emoji[emoji] is None:
                word_emoji[emoji] = [(word, w_e_count)]
            else:
                word_emoji[emoji].append((word, w_e_count))

    return words, emojis, word_emoji

def get_emojis_for_word(word):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""select w.value, e.value, w.count, e.count, w_e.count from words_emojis w_e
                join words w on w_e.words_id = w.id
                join emojis e on w_e.emojis_id = e.id
                where w.value  = ({})""".format(word))
        return _format_result(cursor.fetchall())      

    except Exception as error:
        print(error)
    finally:
        if(connection):
            cursor.close()
            print("closed")

def get_emojis_for_words(word_tuple):


    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('''select w.value, e.value, w.count, e.count, w_e.count from words_emojis w_e
                join words w on w_e.words_id = w.id
                join emojis e on w_e.emojis_id = e.id
                where w.value in {}'''.format(word_tuple))
    
        return _format_result(cursor.fetchall())

    except Exception as error:
        print(error)
    finally:
        if(connection):
            cursor.close()
            print("closed")
