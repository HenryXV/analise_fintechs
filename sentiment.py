import re
import nltk
import pandas as pd
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

# token específico que separa tweets em palavras
tweet_tokenizer = TweetTokenizer()

def stemming(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    palavras = []
    for w in instancia.split():
        palavras.append(stemmer.stem(w))
    return " ".join(palavras)


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


def preprocessing_sentiments(instancia):
    instancia = limpeza_dados(instancia)
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    palavras = [stemming(i) for i in palavras]
    return " ".join(palavras)

def metricas(modelo_m, tweets_m, classes_m):
    resultados = cross_val_predict(modelo_m, tweets_m, classes_m, cv=10)
    return 'Acurácia do modelo: {}'.format(metrics.accuracy_score(classes_m, resultados))


# Tentativa de fazer uma análise simples de sentimentos, mas não de muito certo, por isso não vou incluir, talvez a falta de mais dados ou uma classificação melhor

train = pd.read_csv("./csv/train.csv", index_col=0)
test = pd.read_csv("./csv/nubank_mentions.csv", index_col=0)

tweets = train["text"]
classes = train["score"]
testes = test["text"]

tweets = [preprocessing_sentiments(i) for i in tweets]
testes = [preprocessing_sentiments(i) for i in testes]

vectorizer = CountVectorizer(analyzer="word", tokenizer=tweet_tokenizer.tokenize)
freq_tweets = vectorizer.fit_transform(tweets)

modelo = RandomForestClassifier(n_estimators=10, max_depth=None, random_state=42, min_samples_split=2)
modelo.fit(freq_tweets, classes)

freq_testes = vectorizer.transform(testes)

predicts = modelo.predict(freq_testes)

for t, c in zip(testes, predicts):
    print(t + ", " + str(c))


acc = metricas(modelo, freq_tweets, classes)
print(acc)

