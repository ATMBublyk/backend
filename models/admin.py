from db import db


class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_admins(cls):
        return cls.query.all()
