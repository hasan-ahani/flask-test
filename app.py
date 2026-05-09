from flask import Flask, render_template


app = Flask(import_name=__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_view():
    return render_template('login.html')
    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/forget')
def forget():
    return render_template('forget.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)