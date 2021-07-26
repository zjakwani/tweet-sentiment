from flask_restful import Resource, reqparse
import tweepy


class ApiHandler(Resource):
    def get(self):
        return {"resultStatus": "SUCCESS", "message": "Hello Api Handle"}

    def post(self):
        consumerKey = process.env.consumerKey
        consumerSecret = process.env.consumerSecret
        accessToken = process.env.accessToken
        accessTokenSecret = process.env.accessTokenSecret
        auth = tweepy.OAuthHandler(
            consumer_key=consumerKey, consumer_secret=consumerSecret
        )
        auth.set_access_token(accessToken, accessTokenSecret)
        parser = reqparse.RequestParser()
        parser.add_argument("keyword", type=str)
        parser.add_argument("n", type=str)
        parser.add_argument("message", type=str)

        args = parser.parse_args()

        print(args)
        ret_msg = args["message"]

        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"

        final_ret = {"status": "Success", "message": message}

        # api = tweepy.API(auth)

        # search = args["keyword"]
        # n = int(args["n"])

        # tweets = tweepy.Cursor(api.search, q=search, result_type="recent").items(n)

        # tweetarr = []
        # for t in tweets:
        #     tweetarr.append({"handle": t.user.screen_name, "text": t.text})

        # final_ret = tweetarr

        return final_ret
