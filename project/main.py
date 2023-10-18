from flask import blueprints,Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from . import db
from .model import User,Book,Transaction
from datetime import datetime,date
main=Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    show_book=Book.query.all()
    return render_template('profile.html',name=current_user.email,show_book=show_book)

@main.route('/show_book')
@login_required
def show_book():
    show_book=Book.query.all()
    return render_template('show_book.html',show_book=show_book)

@main.route('/borrow_book/<int:id>',methods=['GET','POST'])
@login_required
def borrow_book(id):
    show_book=Book.query.get(id)

    if request.method=='POST':
        new_borrowed_book=Transaction(book_id_fk=show_book.book_id,user_id_fk=current_user.id,date_issued=datetime.utcnow())
        show_book.availability=False
        db.session.add(new_borrowed_book)
        db.session.commit()
        return redirect(url_for('main.show_book'))  
    else:
        return redirect(url_for('main.show_book'))
    
    
@main.route('/return_book/<int:id>',methods=['GET','POST'])
@login_required
def return_book(id):
    show_book=Book.query.get(id)

    if request.method=='POST':
        # book=Book.query.get(id)
        return_book=Transaction.query.filter_by(book_id_fk=show_book.book_id).first()
        show_book.availability=True
        db.session.delete(return_book)
        db.session.commit()
        return redirect(url_for('main.show_book'))  
    else:
        return redirect(url_for('main.show_book'))