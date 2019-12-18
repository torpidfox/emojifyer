from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from dao import get_emojis, get_emoji_count
from math import log
import re

stemmer = SnowballStemmer("russian")
tokenizer = TweetTokenizer()
total_emoji_count = get_emoji_count()
pseudocount = 5

def _tokenize_sentence(text):
    to_remove = ['.', ',', '"']
    # text = re.sub(r"""[^\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfffА-ЯЁa-zA-Z0-9!?., ]*""",
    #     '', text, flags=re.U)

    tokens = tokenizer.tokenize(text)
    stemmed = []

    for word in tokens:
        stemmed_word = stemmer.stem(word).lower()

        if stemmed_word not in stopwords.words('russian')\
        and stemmed_word not in to_remove\
        and len(stemmed_word) > 1:
            stemmed.append(stemmed_word)

    return stemmed

def _single_naive_bayes_prob(emoji_prob, word_emoji_prob):
    logprob = log(word_emoji_prob / (emoji_prob - word_emoji_prob))

    return logprob

def _emoji_prob(emoji_prob, word_emoji_probs):
    print(emoji_prob)
    print(word_emoji_probs)
    single_probs = sum(_single_naive_bayes_prob(emoji_prob, we_prob) for we_prob in word_emoji_probs)
    return log(emoji_prob / (1 - emoji_prob)) + single_probs


def _emojify_sentence(text):
    stemmed = _tokenize_sentence(text)
    emojis_to_add = []
    stemmed = tuple(stemmed) if len(stemmed) > 1 else stemmed[0]

    words_count, emojis_count, emojis_words_count = get_emojis(stemmed)

    if len(words_count) > 0:
        class_count = len(emojis_count)
        for emoji, emoji_count in emojis_count.items():
            normalizer = emojis_count[emoji] + class_count*pseudocount
            apriori_emoji_prob = (emoji_count + pseudocount) / normalizer

            emoji_logprob = _emoji_prob(apriori_emoji_prob, 
                [we_count / normalizer for word, we_count in emojis_words_count[emoji]])
            if emoji_logprob > 0:
                emojis_to_add.append(emoji)

    return emojis_to_add


def emojify(text):
    emojis_to_add = [_emojify_sentence(s) for s in sent_tokenize(text)]
    result = [t[:-1] + emojis for t, emojis in zip(text, emojis_to_add)] 

    return result


test_text = 'ВДУМАТЬСЯ ТОЛЬКО, КАКОЕ ОХУЕВШЕЕ ЖИВОТНОЕ ОСА!\
ПРИ ДЛИНЕ 1,3 СМ ОНА БЕЗ ПОВОДА НАПАДАЕТ НА ЧЕЛОВЕКА, ТОЛЬКО ЧТОБЫ ПОКАЗАТЬ СВОЮ УДАЛЬ.\
ЭТО КАК, ЕСЛИ БЫ ТЫ УВИДАЛ ВДАЛЕКЕ ВЕЛИКАНА РОСТОМ В 230 МЕТРОВ, ЯРОСТЬ БЫ ЗАСТЛАЛА ТВОИ ГЛАЗА, ТЫ БЫ СХВАТИЛ ТОПОР, ПОДБЕЖАЛ К ВЕЛИКАНУ И УЕБАЛ ЕМУ ПО НОГЕ, КРИЧА:\
"ВОТ ТЕБЕ ЕБАНЫЙ ВЕЛИКАН! ГДЕ ТУТ ТВОЯ ПИЩА? Я СЕЙЧАС СЯДУ НА НЕЕ! ГДЕ ТВОИ ДЕТИ? ДАВАЙ-КА Я ПРИПУГНУ ТОПОРОМ И ИХ! ТВОЯ ЖЕНЩИНА ОТНЫНЕ ВИЗЖИТ ОТ МЕНЯ, ВЕЛИКАН!"\
И ЧТОБЫ ОКОНЧАТЕЛЬНО НАВЕСТИ ШОРОХУ, ТЫ БЫ НАЧАЛ БИТЬСЯ ГОЛОВОЙ О СТЕКЛА, ОБ ПОТОЛОК ВЕЛИКАНОВОГО ЖИЛИЩА, ЧТОБЫ ПОКАЗАТЬ, ЧТО С ТОБОЙ ВООБЩЕ ЛУЧШЕ НЕ СВЯЗЫВАТЬСЯ.\
ПРИМЕРНО ВОТ ТАКОЕ ОХУЕВШЕЕ ЖИВОТНОЕ - ОСА.'
print(emojify(test_text))