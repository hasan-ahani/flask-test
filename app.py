import random
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)


@app.route('/images')
def images():

    images = random.sample(
        range(1, 51), 
        3
        )
    
    return render_template(
        'images.html', 
        images=images
        )






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









USERS = [
    {
        "id": 1,
        "username": "hasan",
        "name": "Hasan Ahani",
        "email": "hasan@gmail.com",
        "password": "1234",  # TODO hash plaintext password
    }
]


@app.route('/')
def index():
    if 'email' not in session:
        return redirect('/login')

    user_found = None
    for user in USERS:
        if user['email'] == session['email']:
            user_found = user
            break

    if user_found is None:
        session.clear()
        return redirect("/login")

    return render_template(
        'index.html',
        name=user_found['name'],
        email=user_found['email'],
        username=user_found['username']
     )









@app.route('/login', methods=["GET", "POST"])
def login_view():
    if 'email' in session:
        return redirect('/')

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "" or password == "":
            return render_template(
                'login.html',
                message="email and password required!"
            )

        user_found = None
        for user in USERS:
            if user['email'] == email:
                user_found = user
                break
        
        if user_found is None:
            return render_template(
                'login.html',
                message="User not found!"
            )
        
        if user_found['password'] != password:
            return render_template(
                'login.html',
                message="User or password invalid!"
            )
        
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
            return render_template(
                'register.html',
                message="All fields are required!"
            )
        
        for user in USERS:
            if user['email'] == email:
                return render_template(
                    'register.html',
                    message="Email already exists!"
                )
        
        new_id = len(USERS) + 1
        new_user = {
            "id": new_id,
            "username": username,
            "name": name,
            "email": email,
            "password": password
        }
        USERS.append(new_user)
        
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