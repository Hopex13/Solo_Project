from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models.user_model import User




class Trip:
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.destination = data['destination']
        self.date = data['date']
        self.flight_class = ['flight_class']
        self.rate = data['rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = User.get_by_id({'id' : self.user_id})


    @classmethod
    def get_all_trips(cls):
        query = "SELECT * FROM trips"
        results = connectToMySQL(DB).query_db(query)
        trips = []
        for trip in results:
            # trip['flight_class'] = trip['flight_class'].strip('[]').strip("'")  # Ensure it's a string, not a list or dict-like
            trips.append(cls(trip))
        
        return trips
        
    
    @classmethod
    def get_trips_by_id(cls, data):
        
        query = "SELECT * FROM trips WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) <1:
            return False
        return cls(result[0])
    

    @classmethod
    def create_trip(cls, data):
        
        query = "INSERT INTO trips (full_name, destination, date,flight_class, rate, user_id, ) VALUES (%(full_name)s, %(destination)s, %(date)s,%(flight_class)s, %(rate)s, %(user_id)s)"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    


    @classmethod
    def update_trip(cls,data):
        query = "UPDATE trips SET full_name=%(full_name)s, destination=%(destination)s, date=%(date)s, rate=%(rate)s, flight_class=%(flight_class)s WHERE id=%(id)s"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    


    @classmethod
    def delete_trip(cls, data):
        query = "DELETE FROM trips WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)
        return results
            
        


      
    @staticmethod
    def validate_trip(data):
        if not data['full_name']:
            flash("Full Name is required.")
            return False
        if not data['destination']:
            flash("Destination is required.")
            return False
        if not data['date']:
            flash("Date is required.")
            return False
        if not data['rate']:
            flash("Rate is required.")
            return False
        if not data['flight_class']:
            flash("Flight Class is required.")
            return False
        return True
   