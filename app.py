from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = 'replace-this-with-something-random-later'
init_db()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not username or not email or not password:
        return "All fields are required."

    hashed_password = generate_password_hash(password)

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        connection.commit()
        connection.close()
        return "Registration successful! <a href='/login'>Log in here.</a>"
    except sqlite3.IntegrityError:
        connection.close()
        return "That username or email is already taken. Go back and try again."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    connection.close()

    if user is None:
        return "No account with that email."

    stored_hashed_password = user[3]

    if check_password_hash(stored_hashed_password, password):
        session['username'] = user[1]
        return redirect('/welcome')
    else:
        return "Incorrect password."

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect('/login')
    return render_template('welcome.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)