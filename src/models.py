from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean, unique=True, nullable=False)
    label = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Todos %r>' % self.done

    def serialize(self):
        return {
            "id": self.id,
            "done": self.done,
            "label": self.label
        }