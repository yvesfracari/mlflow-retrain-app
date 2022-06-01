from .. import db

class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def insert(cls, **kwargs):
        input_data = cls(**kwargs)
        db.session.add(input_data)
        db.session.commit()

    @classmethod
    def order(cls):
        return cls.query.order_by(cls.id.desc())

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def update(cls, id, data):
        cls.query.filter_by(id=id).update(data)
        db.session.commit()
        return cls.find_by_id(id)
