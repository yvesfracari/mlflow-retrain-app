from flask_restx import Namespace, Resource
from flask import jsonify

api = Namespace('hello_world', description="Hello world to test api.")

@api.route('/')
class HelloWorld(Resource):
    @api.doc('Hello world to test api.')
    def get(self,):
        return jsonify({"value": "Hello, World"})
