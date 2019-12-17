import psycopg2
from collections import defaultdict

def get_emojis(word_tuple):


    try:
        connection = psycopg2.connect(user = "postgres", password = "PzZIF5f0kjvR",
                host = "emoji.cqppiab1dnlz.eu-central-1.rds.amazonaws.com",
                port = 5432, database = "emoji_database")

        cursor = connection.cursor()
        cursor.execute('''select w.value, e.value, w.count, e.count, w_e.count from words_emojis w_e
                join words w on w_e.words_id = w.id
                join emojis e on w_e.emojis_id = e.id
                where w.value in {}'''.format(word_tuple))
        
        emojis = defaultdict()
        words = defaultdict()
        word_emoji = defaultdict()
        
        for (word, emoji, w_count, e_count, w_e_count) in cursor.fetchall():
            print(word, emoji, w_count, w_e_count)
            words[word] = w_count
            print(words)
            emojis[emoji] = e_count
            print(emojis)
            if word_emoji[word] is None:
                word_emoji[word] = [(emoji, w_e_count)]
            else:
                word_emoji[word].append((emoji, w_e_count))
            print(word_emoji)
        print(words)
        print(emojis)
        print(word_emoji)

        return words, emojis, word_emoji 

    except Exception as error:
        print(error)
    finally:
        if(connection):
            cursor.close()
            print("closed")


