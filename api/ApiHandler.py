from flask_restful import Resource, reqparse
import tweepy
import os
from textblob import TextBlob
import nltk

nltk.download("punkt")


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
            api.search, q=search, result_type="recent", lang="en"
        ).items(n)

        tweetarr = []
        for t in tweets:
            blob = TextBlob(t.text)
            polarity = blob.sentiment.polarity
            sentiment = ""
            if polarity > 0:
                sentiment = "positive"
            elif polarity < 0:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            tweetarr.append(
                {
                    "handle": t.user.screen_name,
                    "text": t.text,
                    "polarity": polarity,
                    "sentiment": sentiment,
                    "words": blob.words[0],
                }
            )

        return tweetarr
