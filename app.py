import random
import sqlite3
import hashlib
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = 'd39bbd77add1015b501e6fd0f9b7007abad128197d26ac24df98ba39a17ba2dc'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    _ = c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  name TEXT,
                  email TEXT UNIQUE,
                  password TEXT)''')
    _ = c.execute("SELECT * FROM users WHERE email='hasan@gmail.com'")
    if not c.fetchone():
        hashed = hashlib.sha256('1234'.encode()).hexdigest()
        _ = c.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
                  ('hasan', 'Hasan Ahani', 'hasan@gmail.com', hashed))
    conn.commit()
    conn.close()

init_db()

def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    _ = c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()  # pyright: ignore[reportAny]
    conn.close()
    if user:
        return {"id": user[0], "username": user[1], "name": user[2], "email": user[3], "password": user[4]}
    return None

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    _ = c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "username": user[1], "name": user[2], "email": user[3], "password": user[4]}
    return None

def create_user(username, name, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    _ = c.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
              (username, name, email, hashed))
    conn.commit()
    conn.close()

@app.route('/images')
def images():
    images = random.sample(range(1, 51), 3)
    return render_template('images.html', images=images)

@app.route('/table')
def table():
    with open('sales.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    table = []
    for line in lines:
        line = line.strip()
        if line:
            row = line.split(',')
            table.append(row)
    return render_template('table.html', table=table)

@app.route('/')
def index():
    if 'email' not in session:
        return redirect('/login')
    user_found = get_user_by_email(session['email'])
    if user_found is None:
        session.clear()
        return redirect("/login")
    return render_template('index.html', name=user_found['name'], email=user_found['email'], username=user_found['username'])

@app.route('/login', methods=["GET", "POST"])
def login_view():
    if 'email' in session:
        return redirect('/')
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "" or password == "":
            return render_template('login.html', message="email and password required!")
        user_found = get_user_by_email(email)
        if user_found is None:
            return render_template('login.html', message="User not found!")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if user_found['password'] != hashed:
            return render_template('login.html', message="User or password invalid!")
        session['email'] = user_found['email']
        session['username'] = user_found['username']
        return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'email' in session:
        return redirect('/')
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if username == "" or name == "" or email == "" or password == "":
            return render_template('register.html', message="All fields are required!")
        if get_user_by_email(email):
            return render_template('register.html', message="Email already exists!")
        if get_user_by_username(username):
            return render_template('register.html', message="Username already exists!")
        create_user(username, name, email, password)
        session['email'] = email
        session['username'] = username
        return redirect('/')
    return render_template('register.html')

@app.route('/forget')
def forget():
    return render_template('forget.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5001)