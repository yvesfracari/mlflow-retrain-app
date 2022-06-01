import json
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.step import Step
from ..schemas.step import step_schema, steps_schema

api = Namespace('step', description="Step related operations.")

step = api.model('Step', {
    'id': fields.Integer(description="The step identifier", readonly=True),
    'pipeline_id': fields.Integer(description="The pipeline identifier related with this step"),
    'name': fields.String(description="The standardized step name. like: model"),
    'path': fields.String(description="Path of the step function saved"),
})

@api.route("/")
class StepBasic(Resource):
    @api.doc("List all the steps")
    @api.marshal_list_with(step)
    def get(self):
        """List all the steps"""
        steps = Step.query.all()
        return steps_schema.dump(steps)
    
    @api.doc("Create a new step")
    @api.expect(step)
    @api.marshal_with(step, code=201)
    def post(self):
        """Create a new step"""
        input_data = json.loads(request.data)
        new_step = Step(**input_data)
        new_step.save()
        return step_schema.dump(new_step)

@api.route("/<int:id>")
@api.response(404, "Step not found")
@api.param("id", "The step identifier")
class StepInfo(Resource):
    @api.doc("Get a step")
    @api.marshal_with(step, code=201)
    def get(self, id):
        """Get a step given its identifier"""
        step = Step.find_by_id(id)
        return step_schema.dump(step)
    
    @api.doc("Deletes a step")
    @api.response(204, "Step deleted")
    def delete(self, id):
        """Delete a step given its identifier"""
        step = Step.find_by_id(id)
        step.delete()
        return "", 204
    
    @api.expect(step)
    @api.marshal_with(step)
    def put(self, id):
        """Update a step given its identifier"""
        json_data = request.get_json()
        return Step.update(id, dict(json_data))
