from flask import Flask , render_template
app = Flask(__name__)
app.secret_key = "hpx"


@app.route('/')
def home():
    return render_template('index.html')

DB = "flight_schema"