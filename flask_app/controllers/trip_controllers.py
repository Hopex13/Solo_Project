from flask_app import app
from flask import Flask, render_template, redirect , session, request , flash

from flask_app.models.user_model import User
from flask_app.models.trip_model import Trip



#==================== Display Route ==============================
@app.route('/trips/new')
def new_trip():
    return render_template('trip_create.html')


#==================== Actions Route ==============================

@app.route('/trips/add', methods=['POST'])
def create_trip():
    if not Trip.validate_trip(request.form):
        return redirect('/trips/new')
    trip_data = {
        **request.form,
        'user_id': session['user_id']
        
    }
    Trip.create_trip(trip_data)
    return redirect('/trips')

#==================== Display Route ==============================
@app.route('/trips/<int:trip_id>')
def show_one_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/')
    trip = Trip.get_trips_by_id({'id': trip_id})
    user = User.get_by_id({'id': session['user_id']})
    return render_template('details.html', trip=trip, user=user )



#==================== Actions Route ==============================
@app.route('/trips/delete/<int:trip_id>')
def wipe_trip(trip_id):
    Trip.delete_trip({'id': trip_id})
    return redirect('/trips')


