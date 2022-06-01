import json
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.result import Result
from ..schemas.result import result_schema, results_schema

api = Namespace('result', description="Result related operations.")

result = api.model('Result', {
    'id': fields.Integer(description="The result identifier", readonly=True),
    'pipeline_id': fields.Integer(description="The pipeline identifier related with this result"),
    'accuracy': fields.Float(description="The accuracy result on the test"),
    'loss': fields.Float(description="The last loss calculated on the train data"),
})

@api.route("/")
class ResultBasic(Resource):
    @api.doc("List all the results")
    @api.marshal_list_with(result)
    def get(self):
        """List all the results"""
        results = Result.query.all()
        return results_schema.dump(results)
    
    @api.doc("Create a new result")
    @api.expect(result)
    @api.marshal_with(result, code=201)
    def post(self):
        """Create a new result"""
        input_data = json.loads(request.data)
        new_result = Result(**input_data)
        new_result.save()
        return result_schema.dump(new_result)

@api.route("/<int:id>")
@api.response(404, "Result not found")
@api.param("id", "The result identifier")
class ResultInfo(Resource):
    @api.doc("Get a result")
    @api.marshal_with(result, code=201)
    def get(self, id):
        """Get a result given its identifier"""
        result = Result.find_by_id(id)
        return result_schema.dump(result)
    
    @api.doc("Deletes a result")
    @api.response(204, "Result deleted")
    def delete(self, id):
        """Delete a result given its identifier"""
        result = Result.find_by_id(id)
        result.delete()
        return "", 204
    
    @api.expect(result)
    @api.marshal_with(result)
    def put(self, id):
        """Update a result given its identifier"""
        json_data = request.get_json()
        return Result.update(id, dict(json_data))
