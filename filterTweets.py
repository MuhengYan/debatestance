import math
import json
from datetime import datetime
from preProcess import preProcessing


hashtagList = ["#trump2016", "#makeamericagreatagain",
               "#nevertrump", "#dumptrump",
               "#dropouthillary", "#neverhillary",
               "#imwithher", "#hillary2016"]

hashtagTrumpFavor = ["#trump2016", "#makeamericagreatagain"]

hashtagClintonFavor = ["#imwithher", "#hillary2016"]

hashtagTrumpAgainst = ["#nevertrump", "#dumptrump"]

hashtagClintonAgainst = ["#dropouthillary", "#neverhillary"]


def detectTargetHashtags(tweet):
    text = tweet.get("text")
    for tag in hashtagList:
        if tag in text:
            return tweet
    return None

def getTargetStance(tweet):
    tokens = tweet.get("token")
    tweet["favorClinton"] = sum([1 for token in tokens if token in hashtagClintonFavor])
    tweet["favorTrump"] = sum([1 for token in tokens if token in hashtagTrumpFavor])
    tweet["againstClinton"] = sum([1 for token in tokens if token in hashtagClintonAgainst])
    tweet["againstTrump"] = sum([1 for token in tokens if token in hashtagTrumpAgainst])
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
