from . import ma
from ..models.result import Result

class ResultSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "pipeline_id",
            "accuracy",
            "loss",
        )
        model = Result

result_schema = ResultSchema()
results_schema = ResultSchema(many=True)
