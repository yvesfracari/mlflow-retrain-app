from . import ma
from ..models.pipeline import Pipeline

class PipelineSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "created_at",
            "active",
        )
        model = Pipeline

pipeline_schema = PipelineSchema()
pipelines_schema = PipelineSchema(many=True)
