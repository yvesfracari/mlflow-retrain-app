from flask import Blueprint
from flask_restx import Api
from .hello_world import api as hello_word
from .pipeline import api as pipeline
from .version import api as version
from .model import api as model

bp = Blueprint('api', __name__,)
api = Api(bp, api_version="0.1", title="ML Microservice Example Server API",
          description="This is the API for an example of ML model retraining and serving")

api.add_namespace(hello_word)
api.add_namespace(pipeline)
api.add_namespace(version)
api.add_namespace(model)
