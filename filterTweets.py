import math
import json
from datetime import datetime
from preProcess import preProcessing, removeHashtags


hashtagList = ["#trump2016", "#makeamericagreatagain",
               "#nevertrump", "#dumptrump",
               "#dropouthillary", "#neverhillary",
               "#imwithher", "#hillary2016"]

hashtagTrumpFavor = ["#trump2016", "#makeamericagreatagain"]
hashtagClintonFavor = ["#imwithher", "#hillary2016"]
hashtagTrumpAgainst = ["#nevertrump", "#dumptrump"]
hashtagClintonAgainst = ["#dropouthillary", "#neverhillary"]
ht1 = ["#trump2016"]
ht2 = ["#makeamericagreatagain"]
ht3 = ["#imwithher"]
ht4 = ["#hillary2016"]
ht5 = ["#nevertrump"]
ht6 = ["#dumptrump"]
ht7 = ["#dropouthillary"]
ht8 = ["#neverhillary"]
def detectTargetHashtags(tweet):
    text = tweet.get("text")
    hashtagList = ["#trump2016", "#makeamericagreatagain",
                   "#nevertrump", "#dumptrump",
                   "#dropouthillary", "#neverhillary",
                   "#imwithher", "#hillary2016"]
    for tag in hashtagList:
        if tag in text:
            return tweet
    return None

def getTargetStance(tweet):
    tokens = tweet.get("tokens")
    h1 = 0
    h2 = 0
    h3 = 0
    h4 = 0
    h5 = 0
    h6 = 0
    h7 = 0
    h8 = 0
    for token in tokens:
        if token in ht1:
            h1 += 1
        if token in ht2:
            h2 += 1
        if token in ht3:
            h3 += 1
        if token in ht4:
            h4 += 1
        if token in ht5:
            h5 += 1
        if token in ht6:
            h6 += 1
        if token in ht7:
            h7 += 1
        if token in ht8:
            h8 += 1
    fT = h1 + h2
    fC = h3 + h4
    aT = h5 + h6
    aC = h7 + h8
    _tokens = removeHashtags(tokens)
    tweet["tokens"] = _tokens
    tweet["favorClinton"] = fC
    tweet["favorTrump"] = fT
    tweet["againstClinton"] = aC
    tweet["againstTrump"] = aT
    tweet["ht1"] = h1
    tweet["ht2"] = h2
    tweet["ht3"] = h3
    tweet["ht4"] = h4
    tweet["ht5"] = h5
    tweet["ht6"] = h6
    tweet["ht7"] = h7
    tweet["ht8"] = h8
    return tweet

def purgeTweets(tweet):

    text = tweet.get("text")
    tweetId = tweet.get("id_str")
    d2 = datetime.today()
    d1 = datetime.strptime(str(tweet.get("user").get("created_at")), "%a %b %d %H:%M:%S +0000 %Y")
    createdAt = tweet.get("created_at")
    followersCount = float(tweet.get("user").get("followers_count") + 1.0)
    statusesCount = float(tweet.get("user").get("statuses_count"))
    tokens = preProcessing(text)
    retweetCount = 0
    if tweet.get("retweeted_status") and len(tweet.get("retweeted_status")) > 0:
        retweetCount = tweet.get("retweeted_status").get("retweet_count")

    _tweet = {'text': text, 'created_at': createdAt,
              'user_id': tweet.get("user").get("id_str"),
              'retweet_count': retweetCount,
              'id': abs(hash(str(tweetId))),
              'location': tweet.get("user").get("location"),
              'ranking_score': math.log(followersCount) / (statusesCount / (abs(d2 - d1).days + 1.0)),
              'tokens': tokens}

    return _tweet
