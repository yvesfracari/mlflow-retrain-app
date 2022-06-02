import json
import os
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.pipeline import Pipeline
from ..models.version import Version
from ..schemas.pipeline import pipeline_schema, pipelines_schema
from ..scripts.MNIST import MNISTTrain


api = Namespace('pipeline', description="Pipeline related operations.")

pipeline = api.model('Pipeline', {
    'id': fields.Integer(description="The pipeline identifier", readonly=True),
    'name': fields.String(description="The pipeline name"),
    'created_at': fields.DateTime(description="When the pipeline was created", readonly=True),
    'active': fields.Boolean(description="If the pipeline should be used on the model predictions"),
})

pipeline_activation = api.model('Pipeline activation', {
    'name': fields.String(description="The pipeline name"),
})

pipeline_creation = api.model('Pipeline creation', {
    'name': fields.String(description="The pipeline name"),
    'random_seed': fields.Integer(description="The first version random seed."),
})

@api.route("/")
class PipelineBasic(Resource):
    @api.doc("List all the pipelines")
    @api.marshal_list_with(pipeline)
    def get(self):
        """List all the pipelines"""
        pipelines = Pipeline.query.all()
        return pipelines_schema.dump(pipelines)
    
    @api.doc("Create a new pipeline with the first version")
    @api.expect(pipeline_creation)
    @api.marshal_with(pipeline, code=201)
    def post(self):
        """Create a new pipeline with the first version"""
        input_data = json.loads(request.data)
        new_pipeline = Pipeline(name=input_data["name"])
        new_pipeline.save()

        version_dict = {"version_number": 0, 
                        "random_seed": input_data["random_seed"],
                        "pipeline_id": new_pipeline.id,
                        "active": True}

        train = MNISTTrain(random_seed=version_dict["random_seed"])
        results = retrain.train_test()
        name = input_data["name"]
        version_number = version_dict["version_number"]
        path = os.path.join('/files', f"{name}-{version_number}.sav")
        retrain.save_model(path)
        version_dict = {**version_dict, **results, 'path':path}
        new_version = Version(**version_dict)
        new_version.save()
        return pipeline_schema.dump(new_pipeline)

@api.route("/<int:id>")
@api.response(404, "Pipeline not found")
@api.param("id", "The pipeline identifier")
class PipelineInfo(Resource):
    @api.doc("Get a pipeline")
    @api.marshal_with(pipeline, code=201)
    def get(self, id):
        """Get a pipeline given its identifier"""
        pipeline = Pipeline.find_by_id(id)
        return pipeline_schema.dump(pipeline)
    
    @api.doc("Deletes a pipeline")
    @api.response(204, "Pipeline deleted")
    def delete(self, id):
        """Delete a pipeline given its identifier"""
        pipeline = Pipeline.find_by_id(id)
        pipeline.delete()
        return "", 204
    
    @api.expect(pipeline)
    @api.marshal_with(pipeline)
    def put(self, id):
        """Update a pipeline given its identifier"""
        json_data = request.get_json()
        return Pipeline.update(id, dict(json_data))

@api.route("/activation/")
class PipelineActivation(Resource):
    @api.doc("Return the active pipe")
    @api.marshal_list_with(pipeline)
    def get(self):
        """Return the active pipe"""
        pipeline = Pipeline.query.filter_by(active=True).first()
        return pipeline_schema.dump(pipeline)

    @api.doc("Active other pipeline")
    @api.expect(pipeline_activation)
    @api.marshal_with(pipeline, code=201)
    def post(self):
        """Update the active pipeliner"""
        old_active_pipe = Pipeline.query.filter_by(active=True).first()
        if old_active_pipe:
            old_active_pipe.active = False
            old_active_pipe.save()

        new_active_pipe = Pipeline.query.filter_by(name=json.loads(request.data)["name"]).first()
        new_active_pipe.active = True
        new_active_pipe.save()
        return pipeline_schema.dump(new_active_pipe)
