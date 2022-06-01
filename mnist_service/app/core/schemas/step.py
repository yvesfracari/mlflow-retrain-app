from . import ma
from ..models.step import Step


class StepSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "pipeline_id",
            "name",
            "path",
        )
        model = Step

step_schema = StepSchema()
steps_schema = StepSchema(many=True)
