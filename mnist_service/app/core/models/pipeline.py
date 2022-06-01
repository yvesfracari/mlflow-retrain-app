from .. import db
from .utils import BaseModel
from datetime import datetime

class Pipeline(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    random_seed = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Pipeline(id={self.id})"