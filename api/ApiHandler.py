from flask_restful import Resource, reqparse
import tweepy


class ApiHandler(Resource):
    def get(self):
        return {"resultStatus": "SUCCESS", "message": "Hello Api Handle"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("keyword", type=str)
        parser.add_argument("n", type=str)

        args = parser.parse_args()

        print(args)
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

        # request_type = args["type"]
        # request_json = args["message"]
        # # ret_status, ret_msg = ReturnData(request_type, request_json)
        # # currently just returning the req straight
        # ret_status = request_type
        # ret_msg = request_json

        # if ret_msg:
        #     message = "Your Message Requested: {}".format(ret_msg)
        # else:
        #     message = "No Msg"

        # final_ret = {"status": "Success", "message": message}

        consumerKey = process.env.consumerKey
        consumerSecret = process.env.consumerSecret
        accessToken = process.env.accessToken
        accessTokenSecret = process.env.accessTokenSecret
        auth = tweepy.OAuthHandler(
            consumer_key=consumerKey, consumer_secret=consumerSecret
        )
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        search = args["keyword"]
        n = int(args["n"])

        tweets = tweepy.Cursor(api.search, q=search, result_type="recent").items(n)

        tweetarr = []
        for t in tweets:
            tweetarr.append({"handle": t.user.screen_name, "text": t.text})

        final_ret = tweetarr

        return final_ret
