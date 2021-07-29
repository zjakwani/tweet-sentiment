from flask_restful import Resource, reqparse
from flask import jsonify
import tweepy
import os
from textblob import TextBlob
from nltk import FreqDist
from nltk.corpus import stopwords
from dotenv import load_dotenv



load_dotenv()
class ApiHandler(Resource):
    def get(self):
        return {"resultStatus": "SUCCESS", "message": "Hello Api Handle"}

    def post(self):
        consumerKey = str(os.environ.get("consumerKey"))
        consumerSecret = str(os.environ.get("consumerSecret"))
        accessToken = str(os.environ.get("accessToken"))
        accessTokenSecret = str(os.environ.get("accessTokenSecret"))
        auth = tweepy.OAuthHandler(
            consumer_key=consumerKey, consumer_secret=consumerSecret
        )
        auth.set_access_token(accessToken, accessTokenSecret)

        parser = reqparse.RequestParser()
        parser.add_argument("keyword", type=str)
        parser.add_argument("n", type=str)
        args = parser.parse_args()

        api = tweepy.API(auth)
        search = args["keyword"]
        n = int(args["n"])

        tweets = tweepy.Cursor(
            api.search, q=search, result_type="recent", lang="en", tweet_mode="extended"
        ).items(n)

        tweetarr = []
        fulltxt = ""
        for t in tweets:
            text = ""
            try:
                text = t.retweeted_status.full_text
            except AttributeError: 
                text = t.full_text
            polarity = TextBlob(text).sentiment.polarity
            sentiment = "neutral"
            if polarity > 0:
                sentiment = "positive"
            if polarity < 0:
                sentiment = "negative"
            tweetarr.append(
                {
                    "handle": t.user.screen_name,
                    "text": text,
                    "polarity": polarity,
                    "sentiment": sentiment,
                }
            )
            fulltxt += text

        twitter_filter = ["RT", ".", "!", "?" ",", "https", "’", "'s"]
        full_filter = set(twitter_filter + stopwords.words("english"))
        lower_words = [x.lower() for x in TextBlob(fulltxt).words]
        full_words = list(filter(lambda x: x not in full_filter, lower_words))
        common = FreqDist(full_words).most_common(5)

        return jsonify({"tweets": tweetarr, "frequent": common})
