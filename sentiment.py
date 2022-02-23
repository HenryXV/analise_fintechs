import re
import nltk
from nltk.tokenize import TweetTokenizer

# token específico que separa tweets em palavras
tweet_tokenizer = TweetTokenizer()

def limpeza_dados(instancia):
    # remove links, pontos, virgulas,ponto e virgulas dos tweets
    instancia = re.sub(r"http\S+", "", instancia).lower().replace('.', '').replace(';', '').replace('-', '').replace(
        ':', '').replace(')', '')
    return instancia


def preprocessing(instancia):
    instancia = limpeza_dados(instancia)
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return " ".join(palavras)
