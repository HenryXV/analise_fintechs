import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def get_wordcloud(dataframe):
    comment_words = ''
    stopwords = set(STOPWORDS)

    # palavras para ignorar na realização da wordcloud
    stopwords.update(['picpay', 'americanas', 'rt', 'nubank', 'q', 'pra', 'n', 'pagseguro', 'tá', 'vc'])

    # separa cada tweet em palavras individuais, processo de tokenização
    for val in dataframe.text:
        val = str(val)
        tokens = val.split()

        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += ' '.join(tokens)+' '

    wordcloud = WordCloud(width=400, height=400,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    # visualização da wordcloud
    plt.figure(figsize=(8,8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=0)

    plt.show()

