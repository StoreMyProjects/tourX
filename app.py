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
        
        user = db.execute('select username, password, name, email from users where username = ? and password = ?', (username, password))
        rows = user.fetchall()
        for i in rows:
            if username == i[0] and password == i[1]:
                name = i[2]
                email = i[3]
                session["LoggedIn"] = True
                session['name'] = name
                session['username'] = username
                session['email'] = email
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


@app.route('/hotels', methods=['GET','POST'])
def hotels():
    if request.method == "POST":
        star_ratings = request.form.get('ratings')
        room_type = request.form.get('room_type')
        no_of_guests = request.form.get('noOfGuests')
        check_in_date = request.form.get('checkInDate')
        check_out_date = request.form.get('checkOutDate')
        no_of_days = request.form.get('noOfDays')
        try:
            hotels = db.execute("select hotel_id, hotel_name, address, cust_ratings, charges from hotels where ratings = ? and room_type = ? ", (star_ratings, room_type))
            rows = hotels.fetchall()
            return render_template("hotels.html", rows = rows)
        except:
            msg = "No available hotel rooms in this category ! Please try with another category!"
            return render_template("hotels.html", msg = msg)
    return render_template("hotels.html")


@app.route('/flights', methods=['GET','POST'])
def flights():
    if request.method == "POST":
        trip_type = request.form.get('trip_type')
        class_type = request.form.get('class_type')
        departure_d = request.form.get('departure')
        return_d = request.form.get('return')
        source = request.form.get('source')
        destination = request.form.get('destination')
        try:
            flights = db.execute('select flight_name, timing, duration, stops, trip_cost from flights where source = ? and destination = ?', (source, destination))
            rows = flights.fetchall()
            return render_template("flights.html", rows = rows)
        except:
            msg = f"No flights available to {destination} on {departure_d}. Please try another date."
            return render_template('flights.html', msg= msg)
    return render_template("flights.html")

@app.route('/bookings')
def bookingdetails():
    cur = db.cursor()
    cur.execute("SELECT * FROM bookings where username = ?", (session['username']))
    rows = cur.fetchall()
    return render_template("bookings.html", rows = rows)

@app.route('/invoice')
def invoice():
    return render_template("invoice.html")


if __name__ == "__main__":
    app.run(port=5665, debug=True)