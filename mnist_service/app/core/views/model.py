import os
import json
import mlflow
import joblib
import numpy as np
import torch
from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from ..scripts.MNIST import MNISTRetrain


api = Namespace('model', description="Manage and use and MNIST model to new predictions.")

mnist_input = api.model('mnist_input', {
  'image': fields.List(fields.List(fields.Integer(required=True, description='1D flattened array of grey-scaled pixel values, between 0 and 255')))
})

mnist_output = api.model('mnist_output', {
  'digit': fields.Integer(description='the predicted digit, between 0 and 9'),
  'probs': fields.List(fields.Float, description='array of probabilities for each digit, between 0 and 1')
})


@api.route('/')
class MNISTSModel(Resource):
  @api.doc('Use the deployed MNIST model to new predictions')
  @api.expect(mnist_input)
  @api.marshal_list_with(mnist_output)
  def post(self):
    "Use the deployed MNIST model to new predictions"
    data = json.loads(request.data)
    image = torch.from_numpy(np.array(data['image']).astype('float32').reshape(-1, 8, 8))
    output_data = dict()
    output_data['probs'] = current_app.config['model'](image).tolist()
    output_data['digit'] = [prob.index(max(prob)) for prob in output_data['probs']]
    return [dict(zip(output_data,t)) for t in zip(*output_data.values())]

@api.route('/serving/<int:pipeline_id>')
class MNISTServing(Resource):
  @api.doc('Select an MNIST model to be used')
  def get(self, name):
    #TODO: change it to the new database structure
    model_path = os.path.join('/files', "models",f"MNISTmodels-{name}.sav")
    print(model_path, flush=True)
    current_app.config['model'] = joblib.load(model_path)
    return {"Output": "Training complete!",
            "run_name": name,
            "experiment_name": "MNIST"}, 200

  @api.doc('Triger the retraining of the MNIST model and save it on the database.')
  def post(self, name):
    "Retrain the ML model with other random split"
    retrain = MNISTRetrain()
    retrain.train_test(name)
    return {"Output": "Training complete!",
            "run_name": name,
            "experiment_name": "MNIST"}, 200
