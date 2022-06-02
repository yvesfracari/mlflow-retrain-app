import json
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.version import Version
from ..models.pipeline import Pipeline
from ..schemas.version import version_schema, versions_schema

api = Namespace('version', description="Version related operations.")

version = api.model('Version', {
    'id': fields.Integer(description="The version identifier", readonly=True),
    'pipeline_id': fields.Integer(description="The pipeline identifier related with this version"),
    'version_number': fields.Integer(description="The version of the pipeline"),
    'created_at': fields.DateTime(description="When the version was created", readonly=True),
    'path': fields.String(description="Path of the pipeline version function saved"),
    'active': fields.Boolean(description="If the pipeline should be used on the model predictions"),
    'random_seed': fields.Integer(description="The random seed used to split the data"),
    'accuracy': fields.Float(description="The accuracy result on the test"),
    'loss': fields.Float(description="The last loss calculated on the train data"),
})

version_activation = api.model('Version activation', {
    'pipeline_name': fields.String(description="The pipeline name to change the version"),
    'version_number': fields.Integer(description="The version number to activate")
})

@api.route("/")
class VersionBasic(Resource):
    @api.doc("List all the versions")
    @api.marshal_list_with(version)
    def get(self):
        """List all the versions"""
        versions = Version.query.all()
        return versions_schema.dump(versions)
    
    @api.doc("Create a new version")
    @api.expect(version)
    @api.marshal_with(version, code=201)
    def post(self):
        """Create a new version"""
        input_data = json.loads(request.data)
        new_version = Version(**input_data)
        new_version.save()
        return version_schema.dump(new_version)

@api.route("/<int:id>")
@api.response(404, "Version not found")
@api.param("id", "The version identifier")
class VersionInfo(Resource):
    @api.doc("Get a version")
    @api.marshal_with(version, code=201)
    def get(self, id):
        """Get a version given its identifier"""
        version = Version.find_by_id(id)
        return version_schema.dump(version)
    
    @api.doc("Deletes a version")
    @api.response(204, "Version deleted")
    def delete(self, id):
        """Delete a version given its identifier"""
        version = Version.find_by_id(id)
        version.delete()
        return "", 204
    
    @api.expect(version)
    @api.marshal_with(version)
    def put(self, id):
        """Update a version given its identifier"""
        json_data = request.get_json()
        return Version.update(id, dict(json_data))

@api.route("/activation/")
class VersionActivation(Resource):
    @api.doc("Return the active versions")
    @api.marshal_list_with(version)
    def get(self):
        """Return the active pipe"""
        version = Version.query.filter_by(active=True).first()
        return version_schema.dump(version)

    @api.doc("Update the active version of a given pipeline")
    @api.expect(version_activation)
    @api.marshal_with(version, code=201)
    def post(self):
        """Update the active version of a given pipeline"""
        pipeline_id = Pipeline.query.filter_by(name=json.loads(request.data)["pipeline_name"]).first().id
        old_active_version = Version.query.filter_by(active=True, pipeline_id=pipeline_id).first()
        if old_active_version:
            old_active_version.active = False
            old_active_version.save()

        new_active_version = Version.query.filter_by(version_number=json.loads(request.data)["version_number"], pipeline_id=pipeline_id).first()
        new_active_version.active = True
        new_active_version.save()
        return version_schema.dump(new_active_version)
