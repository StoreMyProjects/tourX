from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a1b2c3d4e5f6'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect('tour.db', check_same_thread=False)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.execute('select username, password from users where username = ? and password = ?', (username, password))
        rows = user.fetchall()
        for i in rows:
            if username == i[0] and password == i[1]:
                session["LoggedIn"] = True
                session['username'] = username
                return redirect(url_for("profile"))
        else:
            msg = "User not found! Please enter valid username or password!"
            return render_template("login.html", msg = msg)
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password != confirm:
            error = "password and confirm password do not match."
            return render_template("register.html", error = error)
        else:
            try:
                db.execute('insert into users values(?,?,?,?)', (name, email, username, password))
                db.commit()
                msg = "you are registered successfully!"
                return render_template("register.html", msg = msg)
            except:
                db.rollback()
    return render_template("register.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")    


@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")


@app.route('/destinations')
def destinations():
    return render_template("destinations.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/hotels')
def hotels():
    return render_template("hotels.html")


@app.route('/flights')
def flights():
    return render_template("flights.html")

if __name__ == "__main__":
    app.run(port=5656, debug=True)