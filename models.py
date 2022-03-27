from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tasks(db.Model):

    rowid = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(15), nullable=False)

    def __init__(self, title, date, status):
        super().__init__()
        self.title = title
        self.date = date
        self.status = status

    def __str__(self):
        return f"Titulo:{self.title}\nFecha:{self.date}\nEstado:{self.status}"

    def serialize(self):
        return {
            'rowid': self.rowid,
            'title': self.title,
            'date': self.date,
            'status': self.status
        }

