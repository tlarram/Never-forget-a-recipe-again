from flask import render_template, session,redirect, request,flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe



bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "user_id" in session:
        return redirect('welcome')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pw =bcrypt.generate_password_hash(request.form['password'])
    data={
        **request.form,
        'password': hashed_pw
    }
    session['user_id'] = User.save(data)
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    all_recipes=Recipe.get_all()
    return render_template("home.html", all_recipes=all_recipes, user=user)

@app.route('/destroy/<int:id>')
def destroy_user(id):
    data = {
        "id": id
    }
    User.destroy_user(data)
    return redirect('/welcome')

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect('/')

@app.route('/user/login', methods=['POST'])
def login():
    data= {
        'email' : request.form['email']
    }
    user_from_db=User.get_by_email(data)
    if not user_from_db:
        flash("Invalid Credintials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash("Invalid Credintials", "log")
        return redirect('/')
    session['user_id'] = user_from_db.id
    return redirect(('/welcome'))
    