from .. import db
from .utils import BaseModel
from datetime import datetime

class Pipeline(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Pipeline(id={self.id})"