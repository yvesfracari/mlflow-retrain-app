from . import ma
from ..models.version import Version


class VersionSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "pipeline_id",
            "version_number",
            "created_at",
            "path",
            "active",
            "random_seed",
            "loss",
            "accuracy",
        )
        model = Version

version_schema = VersionSchema()
versions_schema = VersionSchema(many=True)
