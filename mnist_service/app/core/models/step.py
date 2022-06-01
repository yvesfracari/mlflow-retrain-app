from .. import db
from .utils import BaseModel

class Step(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Step(id={self.id})"
