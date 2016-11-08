#Modified from https://bitbucket.org/xidaoW/debatevis_backend/src

import nltk
import string

lmtzr = nltk.WordNetLemmatizer()
stop = nltk.corpus.stopwords.words('english')
stop += ["@", "#"]
punct = [',', '.', ':', ';', '``', '\'\'', 'POS']
skip = [
    '\'s', '\'ve', '\'d', '\'ll', '\'m', '\'re', '(', ')', '>', '<', 'http',
    'almost', '#tweetdebate', '#debate', '#current', '#debate08']



def lemmatize(word):
    return lmtzr.lemmatize(word)


def tokenizer(tweet, takeHashtagMention=True):

    sentences = [sent for sent in nltk.sent_tokenize(tweet)]

    tokens = []
    for sent in sentences:
        tokens += nltk.word_tokenize(sent.lower())
    # lemmatize
    tokens = [
        (
            "".join(l for l in t if l not in string.punctuation.replace("#",""))
            # "".join(l for l in p if l not in string.punctuation)
        ) for t in tokens]

    tokens = [dict(token=t, lemma=lemmatize(t)) for t in tokens]

    #if treat # or @ as tokens
    if takeHashtagMention:
        length = len(tokens)
        for i, token in enumerate(tokens):
            if i + 1 < length:
                if token["lemma"] == "@":
                    tokens[i + 1]["lemma"] = "@" + tokens[i + 1]["lemma"]
                    tokens[i + 1]["token"] = "@" + tokens[i + 1]["token"]
                elif token["lemma"] == "#":
                    tokens[i + 1]["lemma"] = "#" + tokens[i + 1]["lemma"]
                    tokens[i + 1]["token"] = "#" + tokens[i + 1]["token"]

    # removing stopwords
    tokens = [token for token in tokens if token["lemma"] not in stop + skip]

    return tokens

def pre_processing(tweet):
    tokens = tokenizer(tweet)
    return [token["lemma"] for token in tokens \
                    if len(token["lemma"]) > 2 \
                    and token["lemma"][0] not in ['@']]
    # return [token["lemma"] for token in tokens ]
