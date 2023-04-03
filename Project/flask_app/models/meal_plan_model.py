from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import DATABASE
from flask_app.models import user_model
from flask_app.models import recipe_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class Meal_Plan:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.user_id = data['user_id']
        self.start_date = data['start_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_meal_plan(cls, data):
        query= "INSERT INTO meal_plans (name, start_date, user_id) VALUES (%(name)s,%(start_date)s, %(user_id)s);"
        result= connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def update_meal_plan(cls,data):
        query= "UPDATE  meal_plans SET start_date= %(start_date)s, user_id=%(user_id)s WHERE id= %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validator(form_data):
        is_valid= True
        if len(form_data['name']) <1:
            flash('Name Required')
            is_valid = False
        if len(form_data['start_date']) <1:
            flash('Date Required')
            is_valid = False
        return is_valid