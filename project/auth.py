from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from .model import User,Book

auth=Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods=["POST"])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    user=User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password,password):
        flash('please check login details')
        return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('main.profile'))

@auth.route('/signup')  
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
    if request.method=="POST":
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        password=request.form['password']
        email=request.form['email']
        user_type=request.form['user_type']
        user=User.query.filter_by(email=email).first()
        print(email)
        if user:
            flash('email already exits')
            return redirect(url_for('auth.signup'))
        new_user=User(email=email,first_name=firstname,last_name=lastname,user_type=user_type,password=generate_password_hash(password,method='sha256'))
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    
@auth.route('/admin_read',methods=['GET','POST'])
def admin_read():
    if request.method=='POST':
        author=request.form['author']
        title=request.form['title']
        book=Book(author=author,title=title)
        db.session.add(book)
        db.session.commit()
        return redirect('/admin_read')
    
    else:
        lists=Book.query.all()  
        return render_template('admin.html',lists=lists)
    
@auth.route('/admin_delete_book/<int:id>')
def admin_delete_book(id):
    book_to_delete=Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('auth.admin_read'))

@auth.route('/admin_update_book/<int:id>',methods=['POST','GET'])
def admin_update_book(id):
    book_to_update=Book.query.get(id)
    if request.method=="POST":
        book_to_update.title=request.form['title']
        book_to_update.author=request.form['author']
        
        db.session.commit()
        return redirect(url_for('auth.admin_read'))
    else:
        return render_template('admin_update.html',list=book_to_update)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
