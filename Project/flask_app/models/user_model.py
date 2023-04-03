from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query= "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result= connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query= 'SELECT * FROM users;'
        result=connectToMySQL(DATABASE).query_db(query)
        emails = []
        for row in result:
            emails.append(cls(row))
        return emails

    @classmethod
    def destroy_email(cls,data):
        query='DELETE FROM users WHERE id = %(id)s;'
        result= connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def get_by_email(cls,data):
        query ="SELECT * from users WHERE email = %(email)s"
        results= connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query ="SELECT * from users WHERE id = %(id)s"
        results= connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validate(user_data):
        is_valid = True
        if len(user_data['first_name']) <2:
            flash("First name must be complete", "reg")
            is_valid = False
        if len(user_data['last_name']) <2:
            flash("Last name must be complete", "reg")
            is_valid = False
        if len(user_data['email']) < 1:
            flash("Please provide email", "reg")
        elif not EMAIL_REGEX.match(user_data['email']): 
            flash("Invalid email address!")
            is_valid = False
        else:
            data ={
                'email': user_data['email']
            }
            potential_user= User.get_by_email(data)
            if potential_user:
                is_valid= False
                flash("Provided email already has an account, please select forgot password")    
        if len(user_data['password']) <8:
            flash('Passwords must be at least 8 chars','reg')
        elif not user_data['password']== user_data['confirm_pass']:
            flash("Passwords don't match", 'reg')
            is_valid= False
        return is_valid