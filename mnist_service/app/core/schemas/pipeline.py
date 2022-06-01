from . import ma
from ..models.pipeline import Pipeline

class PipelineSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "active",
            "created_at",
            "random_seed",
        )
        model = Pipeline

pipeline_schema = PipelineSchema()
pipelines_schema = PipelineSchema(many=True)
