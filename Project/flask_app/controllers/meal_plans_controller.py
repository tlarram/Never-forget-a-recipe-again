from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.meal_plan_model import Meal_Plan
from flask_app.models.recipe_model import Recipe

@app.route('/mealplans')
def mealplans():
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    all_recipes=Recipe.get_all()
    return render_template("mealplans.html", all_recipes=all_recipes, user=user)
@app.route('/mealplan/new')
def new_meal_plan():
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    return render_template('meal_plan.html', user=user)

@app.route('/mealplan/create', methods=['POST']) #action
def create_meal_plan():
    print(request.form)
    if not "user_id" in session:
        return redirect('/')
    if not Meal_Plan.validator(request.form):
        return redirect('/mealplan/new')
    data={
            **request.form,
            'user_id': session['user_id']
    }
    plan_id=Meal_Plan.save_meal_plan(data)
    return redirect(f'/mealplan/{plan_id}')

@app.route('/mealplan/<int:id>')
def view_meal_plan(id):
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    return render_template('one_meal_plan.html', user=user)