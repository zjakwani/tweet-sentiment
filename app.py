from flask import Flask
from flask_restful import Api

# from flask_cors import CORS  # comment this on deployment
from api.ApiHandler import ApiHandler

app = Flask(__name__)
# CORS(app)  # comment this on deployment
api = Api(app)


api.add_resource(ApiHandler, "/")