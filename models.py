from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tasks(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(16), nullable=False)
    status = db.Column(db.Integer(), nullable=False)

    def __init__(self, title, date, status):
        super().__init__()
        self.title = title
        self.date = date
        self.status = status

    def __str__(self):
        return f"{self.title} -- {self.date} -- {self.status}"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'status': self.status
        }

