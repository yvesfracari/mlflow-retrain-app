from flask import Blueprint
from flask_restx import Api
from .hello_world import api as hello_word
from .MNIST import api as MNIST

bp = Blueprint('api', __name__,)
api = Api(bp, api_version="0.1", title="MLFlow Example Server API",
          description="This is the API for an example of ML model retraining using MLFlow")

api.add_namespace(hello_word)
api.add_namespace(MNIST)
