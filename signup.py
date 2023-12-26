from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    password = request.form['password']
    mobile = request.form['mobile']

    if not name or not dob or not email or not password or not mobile:
        return "Please fill in all the required fields."

    if len(password) < 8:
        return "Password should be at least 8 characters long."

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Store user data in the SQLite database
    new_user = User(name=name, dob=dob, email=email, password=hashed_password, mobile=mobile)
    db.session.add(new_user)
    db.session.commit()

    # Redirect to a success page or do further processing
    return redirect(url_for('success'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
