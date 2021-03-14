from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Notes(db.Model):
   id = db.Column('note_id', db.Integer, primary_key = True)
   title = db.Column(db.String(80))
   content = db.Column(db.Text)

   def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "content": self.content}
