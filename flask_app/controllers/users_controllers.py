from flask_app import app
from flask import Flask , render_template , redirect , request , session, flash
from flask_app.models.user_model import User
from flask_app.models.trip_model import Trip
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)





#================== Display Route =======================
@app.route('/')
def log_reg():
    return render_template('index.html')


#================= Action Routes ==================
@app.route('/create/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user = User.create_user(data)
    session['user_id'] = user

    return redirect('/')

#================= Action Routes ==================
@app.route('/login', methods=['POST'])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid email address or password!!!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect password!!!", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/trips')


#================== Display Route =======================
@app.route('/trips')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    all_trips = Trip.get_all_trips()
    print (all_trips[1].flight_class)
    return render_template("dashboard.html", user=user ,all_trips=all_trips)


#================= Action Routes ==================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/tripss')
def trips():
    return render_template("trips.html")

