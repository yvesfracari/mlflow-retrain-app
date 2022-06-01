from .. import db
from .utils import BaseModel

class Result(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    loss = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Result(id={self.id})"
