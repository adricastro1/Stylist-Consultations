from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Consultation:
    db_name = 'consultation_schema'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.stylist_name = db_data['stylist_name']
        self.date = db_data['date']
        self.event = db_data['event']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator =None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO consultations (stylist_name, date, event, user_id) VALUES (%(stylist_name)s,%(date)s,%(event)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM consultations
                JOIN users ON users.id = consultations.user_id
                WHERE consultations.id = %(id)s
                """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        consultation = cls(results[0])
        owner_data ={
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }
        consultation.creator = User(owner_data)
        return consultation

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM consultations;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        consultations = []
        for consultation in results:
            consultations.append( cls(consultation) )
        return consultations


    @classmethod
    def update(cls,data):
        query = f"UPDATE consultations SET stylist_name=%(stylist_name)s, date=%(date)s, event=%(event)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM consultations WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_consultation(consultation):
        is_valid = True
        if consultation['stylist_name'] == "":
            is_valid = False
            flash("Please choose a stylist","consultation")
        if consultation['date'] == "":
            is_valid = False
            flash("Please choose a date","consultation")
        if len(consultation['event']) < 3:
            is_valid = False
            flash("Event must be at least 3 characters","consultation")
        return is_valid
