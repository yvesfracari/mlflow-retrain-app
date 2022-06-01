import json
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.pipeline import Pipeline
from ..schemas.pipeline import pipeline_schema, pipelines_schema

api = Namespace('pipeline', description="Pipeline related operations.")

pipeline = api.model('Pipeline', {
    'id': fields.Integer(description="The pipeline identifier", readonly=True),
    'name': fields.String(description="The pipeline name"),
    'created_at': fields.DateTime(description="When the pipeline was created", readonly=True),
    'active': fields.Boolean(description="If the pipeline should be used on the model predictions"),
    'random_seed': fields.Integer(description="The random seed used to generate the model"),
})

@api.route("/")
class PipelineBasic(Resource):
    @api.doc("List all the pipelines")
    @api.marshal_list_with(pipeline)
    def get(self):
        """List all the pipelines"""
        pipelines = Pipeline.query.all()
        return pipelines_schema.dump(pipelines)
    
    @api.doc("Create a new pipeline")
    @api.expect(pipeline)
    @api.marshal_with(pipeline, code=201)
    def post(self):
        """Create a new pipeline"""
        input_data = json.loads(request.data)
        new_pipeline = Pipeline(**input_data)
        new_pipeline.save()
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
