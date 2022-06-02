from .. import db
from .utils import BaseModel
from datetime import datetime

class Version(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    path = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    random_seed = db.Column(db.Integer, default=0)
    loss = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Version(id={self.id})"
