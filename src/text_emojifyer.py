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
    stemmed = tuple(stemmed)
    words_count, emojis_count, emojis_words_count = get_emojis(stemmed)

    if len(words_count) > 0:
        class_count = len(emojis_count) + 1
        for emoji, emoji_count in emojis_count.items():
            print(emoji_count)
            print(emojis_words_count[emoji])
            normalizer = emojis_count[emoji] + class_count*pseudocount
            apriori_emoji_prob = (emoji_count + pseudocount) / normalizer

            emoji_logprob = _emoji_prob(apriori_emoji_prob, 
                [(we_count + 1) / normalizer for word, we_count in emojis_words_count[emoji]])
            print(emoji_logprob)
            if emoji_logprob > -1:
                emojis_to_add.append(emoji)

    return emojis_to_add


def emojify(text):
    sentences = sent_tokenize(text)
    emojis_to_add = [_emojify_sentence(s) for s in sentences]
    result = [t[:-1] + ''.join(emojis) for t, emojis in zip(sentences, emojis_to_add)] 

    return result


test_text = 'НАША ЭПОХА - ЭТО ПОТРЕПАННОЕ ПРОШЛОЕ ДЛЯ ЛЮДЕЙ БУДУЩЕГО.КТО ЭТОГО НЕ ПОНИМАЕТ, ТОГО Я И ВИДЕТЬ ТУТ НЕ ХОЧУ.ПРИПОМИНАЕТЕ, КАК В ШКОЛЕ ТЫКАЛИ ПАЛЬЦАМИ В ТОЛСТЫХ ФРАНЦУЗСКИХ КОРОЛЕЙ И УГОРАЛИ НАД ИХ ПАРИКАМИ?"ИОАНН БЕЗЗЕМЕЛЬНЫЙ" - УАХАХА, НИКОЛАЙ, СЛЫШЬ? ПОЗОВИ КОЛЯНА! (ШЕПОТОМ). "КОЛЯН БЕЗХУЙИЙ!" - И ПОШЛА ПОТЕШКА, ПОКА УЧИТЕЛЬ ЛИНЕЙКОЙ ПАЛЬЦЫ НЕ ПООТШИБАЕТ.ТАК ЖЕ НАД НАШЕЙ ЭПОХОЮ УГОРАТЬ СТАНУТ.1. ЭТО, ДЕТИ, ФОТОКАРТОЧКА ЗАКЛАДОШНИКА! В ТУ ПОРУ В РОССИИ ОБИТАЛО ЦЕЛОЕ СОСЛОВИЕ ЛЮДЕЙ, ДОСТАВЛЯЮЩИХ ВЕЩЕСТВА, КОТОРЫЕ БЫЛИ ЗАПРЕЩЕНЫ И НАЗЫВАЛИСЬ "НАРКОТА!". ЗАКЛАДОШНИКА ЧУРАЛИСЬ, ОН СЧИТАЛСЯ ОТВЕРЖЕННЫМ, ЖЕНЩИНЫ НЕ ХОТЕЛИ ИМЕТЬ С НИМ ПАРТИИ, ЧТО ПРИДАВАЛО ЗАКЛАДОШНИКАМ, ОДНАКО, НЕКИЙ РОМАНТИЧЕСКИЙ ФЛЕР. ПРО НИХ СЛАГАЛИ БАЛЛАДЫ В ПОПУЛЯРНОМ ТОГДА ЖАНРЕ КЛАУД РЕП!САМАЯ ИЗВЕСТНАЯ - ЭТО КОМПОЗИЦИЯ 2023 ГОДА:"ОХ КАКАЯ СЛАДКАЯ, МОЯ ЗАКЛАДКА, МА!"ЭТОТ ФОЛЬКЛОР ВЫ, НАВЕРНЯКА, ПОМНИТЕ - МЫ ЕГО НА УРОКАХ ПЕНИЯ СОЛЬФЕДЖО ИСПОЛНЯЛИ В ДВАДЦАТЬ ГОРЛ. ИЗ ГОРРОНО ТЕТЕЧКА В ЧОКЕРЕ ПЛАКАЛА ЕЩЕ.2. А ЭТО, ДЕТИ, ФАВОРИТКА ПРАВИТЕЛЯ РОССИИ - МАРКИЗА АНАСТАСИЯ ПЕРВАЯ ИВЛЕЕВА. ПОСЛЕ ОТСТРАНЕНИЯ ОТ ВЛАСТИ ВЛАДИМИРА СТАБИЛЬНОГО, ТРОН ЗАНЯЛ АЛЕКСЕЙ НАВАЛЬНЫЙ, КОТОРЫЙ В 2029 ГОДУ ПРЕВОЗГЛАСИЛ СЕБЯ ГОСУДАРЕМ РОССИИ, БЕЛОРУССИИ, УКРАИНЫ И ИНЫХ ОКРЕСТНЫХ СТРАН, МОРЕЙ И НЕБЕСНЫХ ТЕЛ, ВЫГНАЛ ВЗАШЕЙ ЖЕНУ И ВЗЯЛ К СЕБЕ ИВЛЕЕВУ, А ПАЖЕМ К НЕЙ ИМЕНИТОГО ГЛАШАТАЯ, ПОЗЖЕ ЛИЧНОГО КОРОЛЕВСКОГО ШУТА - ЭЛДЖЕЯ. ПОСЛЕ ИВЛЕЕВА ОТРАВИЛА НАВАЛЬНОГО, А ЭЛДЖЕЯ ОСКОПИЛА И СДАЛА В МОНАСТЫРЬ, ПОСЛЕ ЧЕГО ПРАВИЛА 16 ЛЕТ ДО ЗНАМЕНИТЫХ ТИНДЕРСКИХ ПОГРОМОВ.4. ПРИЧИСЛЕНИЕ КОКЛЮШКИНА К ЛИКУ СВЯТЫХ НОЯБРЬ 2030. ИСТОРИЧЕСКИХ ДОКУМЕНТОВ НЕ ОСТАЛОСЬ.5. А ВОТ КАДРЫ ЗНАМЕНИТОГО ИСЧЕЗНОВЕНИЯ КОШЕК.ДО 2056 ГОДА, ДЕТИ, ПОЧТИ В КАЖДОМ ДОМЕ И ПОДВАЛЕ ОБИТАЛИ НЕКИЕ УСАТЫЕ ЖИВОТНЫЕ ПО ИМЕНИ "КОШКА". БЫЛИ ОНИ ПЫШНЫЕ, ВАЖНЫЕ КАК ДЕПУТАТЫ МОСГОРДУМЫ, НЕЖИЛИСЬ НА БАТАРЕЕ И ЖИЛИ ПРАЗДНО, БЕЗ НАДРЫВА. А ПОТОМ 12 СЕНТЯБРЯ 2056 СОБРАЛИСЬ И ВЫШЛИ ВСЕ ПРОЧЬ И БОЛЬШЕ ИХ НИКТО С ТЕХ ПОР И НЕ ВИДЫВАЛ. А ВМЕСТЕ С НИМИ И КУКЛАЧЕВ ПРОПАЛ.5. А ВОТ ЗНАТНЫЙ ШАРЛАТАН - ИЛОН МАСК, ЧТО МОРОЧИЛ ЛЮДЯМ ГОЛОВУ О ПОЛЕТАХ НА МАРС, БЕСПИЛОТНЫХ АВТОМОБИЛЯХ, ВАКУУМНЫХ ТОННЕЛЯХ. КОГДА АФЕРЫ РАСКРЫЛИСЬ, БЕЖАЛ СО СВОИМ ТАЙНЫМ ЛЮБОВНИКОМ ДЖАСТИНОМ ТИМБЕРЛЕЙКОМ ВО ФРАНЦУЗСКУЮ ГВИАНУ, ОТКУДА В 2041 ГОДУ БЫЛ ДОСТАВЛЕН СПЕЛЕНУТЫМ В ГУАНТАНАМО, НЫНЕ ТЕРРИТОРИЯ ФША (ФЕМИНИСТИЧЕСКИЕ ШТАТЫ АМЕРИКИ)НО, ДЕТИ, ДОВОЛЬНО, ДОСТАЕМ ПОЛОВИНКУ ЛИСТОЧКА В КЛЕТОЧКУ И ПИШЕМ ДИКТАНТ НА ТЕМЫ:1. ЛИРИКА РАННЕГО ОКСИМИРОНА В ЭПОХУ ДИКТАТА ГРАЙМА2. СТАНОВЛЕНИЕ ФЕЙСИТИНГА В КОНЦЕ ДЕСЯТЫХ ГОДОВ 21-ГО ВЕКАP.S. ВПРОЧЕМ, ЧТО-ТО Я РАЗДУХАРИЛСЯ. ЕСЛИ СЛУЧИТСЯ МНЕ УГОДИТЬ В ШКОЛЬНУЮ ПРОГРАММУ, ТО К МОЕМУ ПОРТРЕТУ В ИЗДАНИИ "РОДНИЧОК РОДНАЯ РЕЧЬ" ДЕТИ БУДУТ ПОДРИСОВЫВАТЬ УСЫ, ХУЙЦЫ.НЕ ПОТОМУ ЧТО ПЛОХОЙ ПИСАТЕЛЬ, НО ПОТОМУ ЛИШЬ, ЧТО ДЕТИ - ТАКАЯ БЕСЦЕРЕМОННАЯ ПУБЛИКА, КОЛИ ЕСТЬ РУЧКА ДА ПОВЕРХНОСТЬ, НЕПРЕМЕННО ХУЕЦ ИЗОБРАЗЯТ ИЛИ МОРДОЧКУ КАКУЮ.'
print(emojify(test_text))