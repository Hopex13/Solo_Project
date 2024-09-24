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
            trip['flight_class'] = trip['flight_class'].strip('[]').strip("'")  # Ensure it's a string, not a list or dict-like
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
        
        query = "INSERT INTO trips (full_name, destination, date, rate, user_id, flight_class) VALUES (%(full_name)s, %(destination)s, %(date)s, %(rate)s, %(user_id)s,%(flight_class)s)"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    


    @classmethod
    def delete_trip(cls, data):
        query = "DELETE FROM trips WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)
        return results
            
        


      
    @staticmethod
    def validate_trip(data):
        is_valid = True
        if len(data['full_name']) < 3:
            flash("Full Name must be at least 3 characters", "register")
            is_valid = False


        if len(data['destination']) < 3:
            flash("Destination must be at least 3 characters", "register")
            is_valid = False
        
        
        if len(data['rate']) < 3:
            flash("Rate must be at least 3 characters", "register")
            is_valid = False
        return is_valid

   