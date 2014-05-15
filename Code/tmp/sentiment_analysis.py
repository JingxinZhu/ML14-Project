import sys
import collections

import numpy as np

from nltk.tokenize import word_tokenize as wt
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

import logging, gensim, bz2

def clean_tokens():
    n_topics = 25

    # get all tweets
    tw = [line.strip('\n') for line in file('corpus_full')]

    # lower case and tokenize
    print 'Lower casing'
    tokens = [[word.lower() for word in wt(tt)] for tt in tw]

    # filter punctuations
    print 'Filtering punctuations'
    punc = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*',\
            '@', '#', '$', '%']
    tokens_unpunc = [[w for w in tk if not w in punc] for tk in tokens]

    # filter stopping words
    print 'Filtering stopping words'
    english_stopwords = stopwords.words('english')
    tokens_filtered = [[w for w in tk if not w in english_stopwords] for tk in\
            tokens_unpunc]

    # stemming
    print 'Stemming words'
    st = LancasterStemmer()
    tokens_stemmed = [[st.stem(w) for w in tk] for tk in tokens_filtered]

    # eliminate words with count == 1
    '''
    print 'Eliminating words appear once'
    all_items = sum(tokens_stemmed, [])
    print len(all_items)
    print 'Building once'
    once = set(t for t in set(all_items) if all_items.count(t) == 1)
    print 'Generating final tokens'
    final_tokens = [[s for s in tk if s not in once] for tk in tokens_stemmed]
    '''

    # eliminate some specific words and words that appear only once
    count = collections.defaultdict(int)
    for t in tokens_stemmed:
        for w in t:
            if w == 'http' or w[0 : 6] == '//t.co':
                print w
            else:
                count[w] += 1
    tokens_stemmed = [[st.stem(w) for w in tk] for tk in tokens_filtered]
    tokens_final = [[w for w in tk if count[w] > 1] for tk in tokens_stemmed]

    # LDA
    logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s',\
            level = logging.INFO)
    dictionary = gensim.corpora.Dictionary(tokens_final)
    print 'Building corpus for LDA'
    corpus = [dictionary.doc2bow(t) for t in tokens_final]
    print 'LDA'
    lda = gensim.models.ldamodel.LdaModel(corpus = corpus, id2word = dictionary,
            num_topics = n_topics)
    print lda.print_topics()


    # extract topics for tweets
    topic_matrix = []
    for i in range(98900):
        topics = lda[dictionary.doc2bow(tokens_final[i])]
        v = [0.] * n_topics
        for t in topics:
            v[t[0]] = t[1]
        topic_matrix.append(v)

    # write matrix to the disk
    np.save('topic_matrix', topic_matrix)

    # write topics to the disk
    topics = lda.show_topics(-1)
    with open('topics', 'a') as f:
        for i, t in enumerate(topics):
            f.write(str(i) + '-' + t + '\n')

if __name__ == '__main__':
    print 'hello'
else:
    clean_tokens()
