from flask import Blueprint
from flask_restx import Api
from .hello_world import api as hello_word
from .model import api as model
from .result import api as result
from .step import api as step
from .pipeline import api as pipeline

bp = Blueprint('api', __name__,)
api = Api(bp, api_version="0.1", title="ML Microservice Example Server API",
          description="This is the API for an example of ML model retraining and serving")

api.add_namespace(hello_word)
api.add_namespace(model)
api.add_namespace(pipeline)
api.add_namespace(step)
api.add_namespace(result)
