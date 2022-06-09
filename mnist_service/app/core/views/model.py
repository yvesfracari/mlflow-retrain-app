import os
import json
import joblib
import numpy as np
import torch
from torchvision.transforms import Normalize
from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from ..models.pipeline import Pipeline
from ..models.version import Version


api = Namespace('model', description="Manage and use and MNIST model to new predictions.")

mnist_input = api.model('mnist_input', {
  'images': fields.List(fields.List(fields.List(fields.Float(required=True, description='3D array of grey-scaled pixel values, between 0 and 255'))))
})

mnist_output = api.model('mnist_output', {
  'digit': fields.Integer(description='the predicted digit, between 0 and 9'),
  'probs': fields.List(fields.Float, description='array of probabilities for each digit, between 0 and 1')
})

@api.route('/')
class MNISTSModel(Resource):
  @api.doc('Use the active MNIST model to new predictions')
  @api.expect(mnist_input)
  @api.marshal_list_with(mnist_output)
  def post(self):
    "Use the deployed MNIST model to new predictions"
    data = json.loads(request.data)
    images = torch.FloatTensor(data['images'])
    pipeline_id = Pipeline.query.filter_by(active=True).first().id
    version_path = Version.query.filter_by(pipeline_id=pipeline_id, active=True).first().path
    model = joblib.load(version_path)
    output_data = dict()
    scaler = Normalize((0.1307,), (0.3081,))
    output_data['probs'] = model(scaler(images)).tolist()
    output_data['digit'] = [prob.index(max(prob)) for prob in output_data['probs']]
    return [dict(zip(output_data,t)) for t in zip(*output_data.values())]
