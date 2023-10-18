from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(20),nullable=False)
    last_name=db.Column(db.String(20),nullable=False)
    # phone=db.Column(db.Integer,unique=True,nullable=False)
    password=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(120),nullable=False)    
    user_type=db.Column(db.String(20),nullable=False)
    users=db.relationship('Transaction',backref="user",lazy=True)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"

class Book(db.Model):
    book_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    author=db.Column(db.String(20),nullable=False,default='na')
    availability=db.Column(db.Boolean,default=True,nullable=False)
    books=db.relationship('Transaction',backref='book',lazy=True)

class Transaction(db.Model):
    transaction_id=db.Column(db.Integer,primary_key=True)
    book_id_fk=db.Column(db.Integer,db.ForeignKey("book.book_id"))
    user_id_fk=db.Column(db.Integer,db.ForeignKey("user.id"))
    date_issued=db.Column(db.DateTime(),nullable=True)
    date_returned=db.Column(db.DateTime(),nullable=True)


    






