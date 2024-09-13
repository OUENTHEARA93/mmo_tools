from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FacebookAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100))
    page_name = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    reached = db.Column(db.Integer)
    page_url = db.Column(db.String(200))
    created_date = db.Column(db.String(50))
    monetization = db.Column(db.String(20))
    description = db.Column(db.Text)
