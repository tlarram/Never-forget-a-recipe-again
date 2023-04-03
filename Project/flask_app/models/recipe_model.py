from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import DATABASE
from flask_app.models import user_model



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions= data['instructions']
        self.date_cooked = data['date_cooked']
        self.cook_time = data['cook_time']
        self.ingredients= data['ingredients']
        self.user_id= data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_recipe(cls, data):
        query= "INSERT INTO recipes (name, description, instructions, date_cooked, cook_time, ingredients, user_id) VALUES (%(name)s, %(description)s, %(instructions)s,%(date_cooked)s,%(cook_time)s, %(ingredients)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
        

    @classmethod
    def update(cls,data):
        query= "UPDATE  recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s,  ingredients=%(ingredients)s, cook_time=%(cook_time)s WHERE id= %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM recipes JOIN users on users.id=recipes.user_id"
        results= connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes =[]
            for row in results:
                this_recipe=cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at']
                }
                this_user=user_model.User(user_data)
                this_recipe.poster = this_user
                all_recipes.append(this_recipe)
            return all_recipes
        return results
    
    @classmethod
    def get_by_id(cls,data):
        query ="SELECT * from recipes JOIN users on users.id=recipes.user_id WHERE recipes.id = %(id)s"
        results= connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        row=results[0]    
        this_recipe= cls(row)
        user_data= {
            **row,
            'id': row['users.id'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        }
        this_user=user_model.User(user_data)
        this_recipe.poster=this_user
        return this_recipe

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id= %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validator(form_data):
        is_valid= True
        if len(form_data['name']) <1:
            flash('Title Required')
            is_valid = False
        if len(form_data['description']) <1:
            flash('Description Required')
            is_valid = False
        if len(form_data['instructions']) <1:
            flash('Instructions Required')
            is_valid = False
        if len(form_data['date_cooked']) <1:
            flash('Date Required')
            is_valid = False
        if "cook_time" not in form_data:
            flash("Cook time required")
            is_valid = False
        return is_valid
    
    