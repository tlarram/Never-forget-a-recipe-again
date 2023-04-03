from flask import render_template, session,flash,redirect, request, jsonify
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
import requests
import os

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': os.environ.get("FLASK_APP_API_KEY"),
}
random_joke = "food/jokes/random"
find = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
randomFind = "recipes/random"

bcrypt = Bcrypt(app)

@app.route('/recipeshome')
def recipes_home():
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    all_recipes=Recipe.get_all()
    return render_template("recipes_home.html", all_recipes=all_recipes, user=user)

@app.route('/recipe/new')
def new_recipe_form():
    if not "user_id" in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    return render_template('new_recipe.html', user=user)

@app.route('/recipe/create', methods=['POST']) #action
def create_recipe():
    if not "user_id" in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipe/new')
    data={
            **request.form,
            'user_id': session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/welcome')

@app.route('/api/recipe/create', methods=['POST']) #action
def api_create_recipe():
    if not "user_id" in session:
        return redirect('/')
    print(request.form)
    data={
            **request.form,
            'user_id': session['user_id']
    }
    user=User.get_by_id({'id': session['user_id']})
    recipe_id=Recipe.save_recipe(data)
    res={
        'msg': 'success',
        'form': data,
        'recipe_id': recipe_id,
        'poster':f"{user.first_name}"
        }
    return jsonify(res)

@app.route('/recipe/<int:id>/edit')
def update_recipe_form(id):
    if not "user_id" in session:
        return redirect('/')
    recipe= Recipe.get_by_id({'id':id})
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipe/<int:id>/update', methods=['POST']) #action
def update_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f'/recipe/{id}/edit')
    data={
        **request.form,
        'id':id
    }
    Recipe.update(data)
    return redirect('/welcome')

@app.route('/api/recipe/<int:id>/update', methods=['POST']) #action
def api_update_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    print(request.form)
    data={
            **request.form,
            'user_id': session['user_id']
    }
    user=User.get_by_id({'id': session['user_id']})
    recipe_id=Recipe.update(data)
    res={
        'msg': 'success',
        'form': data,
        'recipe_id': recipe_id,
        'poster':f"{user.first_name}",
         'id':id
        }
    return jsonify(res)

@app.route("/recipe/<int:id>/view")
def show_one_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    data={
        'id':id
    }
    user= User.get_by_id({'id':session['user_id']})
    recipe =Recipe.get_by_id(data)
    return render_template("one_recipe.html", recipe=recipe, user=user)

@app.route('/joke')
def search_page():
    joke_response = str(requests.request("GET", url + random_joke, headers=headers).json()['text'])
    return render_template('search.html', joke=joke_response)

@app.route('/recipes')
def get_recipes():
    if (str(request.args['ingredients']).strip() != ""):
    # If there is a list of ingridients -> list
        querystring = {"ingredients":request.args['ingredients'],"number":"5","ignorePantry":"true","ranking":"1"}
        response = requests.request("GET", find, headers=headers, params=querystring).json()
        return render_template('apirecipes.html', recipes=response)
    else:
    # Random recipes
        querystring = {"number":"5"}
        response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
        print(response)
        return render_template('apirecipes.html', recipes=response['recipes'])

@app.route('/recipe/<int:id>/delete')
def delete_party(id):
    if not "user_id" in session:
        return redirect('/')
    data={
        'id':id
    }
    deleted=Recipe.get_by_id(data)
    if not session['user_id'] == deleted.user_id:
        flash("Quit tryiong to delete other people's stuff")
        return redirect('/')
    Recipe.delete(data)
    return redirect("/welcome")


@app.route('/recipe')
def api_get_recipe():
  recipe_id = request.args['id']
  recipe_endpoint = "recipes/{0}/information".format(recipe_id)
  nutritionWidget = "recipes/{0}/nutritionWidget".format(recipe_id)
  recipe_info = requests.request("GET", url + recipe_endpoint, headers=headers).json()
    
  recipe_headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': os.environ.get("FLASK_APP_API_KEY"),
      'accept': "text/html"
  }
  querystring = {"defaultCss":"true", "showBacklink":"false"}
  recipe_info['nutritionWidget'] = requests.request("GET", url + nutritionWidget, headers=headers, params=querystring).text
    
  return render_template('api_recipe.html', recipe=recipe_info)
