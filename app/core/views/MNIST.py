import json
import mlflow
import numpy as np
from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from ..scripts.MNIST import MNISTRetrain


api = Namespace('MNIST', description="Manage and use and MNIST model to new predictions.")

mnist_input = api.model('mnist_input', {
  'image': fields.List(fields.Integer, required=True, description='1D flattened array of grey-scaled pixel values, between 0 and 255')
})

mnist_output = api.model('mnist_output', {
  'digit': fields.Integer(description='the predicted digit, between 0 and 9'),
  'probas': fields.List(fields.Float, description='array of probabilities for each digit, between 0 and 1')
})


@api.route('/')
class MNISTPredict(Resource):
  @api.doc('Use the deployed MNIST model to new predictions')
  @api.expect(mnist_input)
  @api.marshal_list_with(mnist_output)
  def post(self):
    "Use the deployed MNIST model to new predictions"
    data = json.loads(request.data)
    image = np.array(data['image']).astype('float32').reshape(1, 8, 8)
    output_data = dict()
    import pdb
    pdb.set_trace()
    output_data['probas'] = current_app.config['model'].predict(image).tolist()
    output_data['digit'] = output_data['probas'].index(max(output_data['probas']))
    return jsonify(output_data)


@api.route('/model_management/<string:name>')
class MNISTModelManagement(Resource):
  @api.doc('')
  def get(self, name):
    experiment_id = mlflow.get_experiment_by_name(name="MNIST").experiment_id
    df_runs = mlflow.search_runs([experiment_id])
    df_run = df_runs[df_runs['tags.mlflow.runName'] == name]
    run_id = df_run['run_id'].values[0]
    current_app.config['model'] = mlflow.pyfunc.load_model(model_uri=f"static/mlruns/{experiment_id}/{run_id}/artifacts/model")
    return jsonify(df_run.to_dict())

  @api.doc('')
  def post(self, name):
    "Retrain the ML model with other random split"
    retrain = MNISTRetrain()
    retrain.train_test(name)
    return {"Output": "Training complete!",
            "run_name": name,
            "experiment_name": "MNIST"}, 200
