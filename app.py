from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import sqlite3
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a1b2c3d4e5f6'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect('tour.db', check_same_thread=False)

time_now = time.localtime()
time_now = str(time_now.tm_hour) + ":" + str(time_now.tm_min)

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
                msg = "something wrong happend while registering! Please try Again!"
            finally:
                db.rollback()
                return render_template("register.html" ,msg = msg)
    return render_template("register.html")


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    if request.method == "POST":
        if request.form.get("selected_package") == "Spain":
            package_name = "Spain Package"
            place = "Barcelona"
            num_of_days = 10
            estimated_cost = 220000

        elif request.form.get("selected_package") == "India":
            package_name = "India Package"
            place = "Goa"
            num_of_days = 10
            estimated_cost = 153000

        elif request.form.get("selected_package") == "Switzerland":
            package_name = "Switzerland Package"
            place = "Zurich"
            num_of_days = 10
            estimated_cost = 117500

        elif request.form.get("selected_package") == "Belgium":
            package_name = "Belgium Package"
            place = "Dinant"
            num_of_days = 8
            estimated_cost = 213000

        elif request.form.get("selected_package") == "Italy":
            package_name = "Italy Package"
            place = "Venice"
            num_of_days = 8
            estimated_cost = 118000

        elif request.form.get("selected_package") == "Australia":
            package_name = "Australia Package"
            place = "Sydney"
            num_of_days = 8
            estimated_cost = 210000

        elif request.form.get("selected_package") == "Ireland":
            package_name = "Ireland Package"
            place = "Dublin"
            num_of_days = 8
            estimated_cost = 119000

        elif request.form.get("selected_package") == "New Zealand":
            package_name = "New Zealand Package"
            place = "Mount Cook"
            num_of_days = 8
            estimated_cost = 217000

        elif request.form.get("selected_package") == "Canada":
            package_name = "Canada Package"
            place = "Big Muddy Valley"
            num_of_days = 5
            estimated_cost = 187100

        elif request.form.get("selected_package") == "Venezuela":
            package_name = "Venezuela Package"
            place = "Angel Falls"
            num_of_days = 5
            estimated_cost = 115000

        elif request.form.get("selected_package") == "Arizona":
            package_name = "Arizona Package"
            place = "Tucson"
            num_of_days = 5
            estimated_cost = 215000

        elif request.form.get("selected_package") == "Norway":
            package_name = "Norway Package"
            place = "Bergen"
            num_of_days = 10
            estimated_cost = 210000

        elif request.form.get("selected_package") == "Myanmar":
            package_name = "Myanmar Package"
            place = "Shwedagon Pagoda"
            num_of_days = 8
            estimated_cost = 211000

        elif request.form.get("selected_package") == "Namibia":
            package_name = "Namibia Package"
            place = "Namibia"
            num_of_days = 8
            estimated_cost = 117300

        elif request.form.get("selected_package") == "French Polynesia":
            package_name = "French Polynesia Package"
            place = "Skeleton Coast"
            num_of_days = 5
            estimated_cost = 215700

        elif request.form.get("selected_package") == "Iceland":
            package_name = "Iceland Package"
            place = "Skogafoss"
            num_of_days = 10
            estimated_cost = 218200

        elif request.form.get("selected_package") == "Greece":
            package_name = "Greece Package"
            place = "Athens"
            num_of_days = 9
            estimated_cost = 214800

        elif request.form.get("selected_package") == "China":
            package_name = "China Package"
            place = "Beijing"
            num_of_days = 6
            estimated_cost = 115900

        elif request.form.get("selected_package") == "Germany":
            package_name = "Germany Package"
            place = "Berlin"
            num_of_days = 5
            estimated_cost = 116500

        else:
            package_name = "Chile Package"
            place = "Easter Island"
            num_of_days = 8
            estimated_cost = 119000

        try:
            with sqlite3.connect('tour.db') as db:
                db.execute("Insert into destinations values(null,?,?,?,?,?,?,?)",( session['email'], package_name, place, num_of_days, estimated_cost, time_now , session['username'] ))
                db.commit()       
            msg = "package added successfully!"
            return render_template('hotels.html', msg = msg)
        except:
            msg = "Something went wrong while adding package!"
            return render_template("destinations.html", msg = msg)

    return render_template("destinations.html")


@app.route('/hotels', methods=['GET','POST'])
def hotels():
    if request.method == "POST":
        cost = request.form.get('cost')
        category = request.form.get('category')
        room_type = request.form.get('room_type')
        no_of_guests = request.form.get('noOfGuests')
        check_in_date = request.form.get('checkIn')
        check_out_date = request.form.get('checkOut')
        no_of_days = request.form.get('noOfDays')
        try:
            with sqlite3.connect('tour.db') as db:
                db.execute("insert into hotels values(null,?,?,?,?,?,?,?,?,?)",(session["email"], cost, category, room_type, no_of_guests, check_in_date, check_out_date, no_of_days, session["username"]))
                db.commit()
            msg = "hotel room booked successfully!"
            return render_template('flights.html', msg = msg)
            # hotels = db.execute("select hotel_id, hotel_name, address, cust_ratings, charges from hotels where ratings = ? and room_type = ? ", (star_ratings, room_type))
            # rows = hotels.fetchall()
            # return render_template("hotels.html", rows = rows)
        except:
            msg = "Something went wrong while booking hotel room!"
            # msg = "No available hotel rooms in this category ! Please try with another category!"
            return render_template("hotels.html", msg = msg)
    return render_template("hotels.html")


@app.route('/flights', methods=['GET','POST'])
def flights():
    if request.method == "POST":
        trip_type = request.form.get('trip_type')
        class_type = request.form.get('class_type')
        departure_d = request.form.get('departure')
        return_d = request.form.get('return')
        passengers = request.form.get('passengers')
        source = request.form.get('source')
        destination = request.form.get('destination')
        try:
            with sqlite3.connect('tour.db') as db:
                db.execute("insert into flights values(null,?,?,?,?,?,?,?,?,?)",(session['email'], trip_type, class_type, departure_d, return_d, passengers, source, destination, session['username']))
                db.commit()
            return redirect(url_for('payment'))
            # msg = "flights booked succesfully!"
            # return render_template("payment.html", msg = msg)
            # flights = db.execute('select flight_name, timing, duration, stops, trip_cost from flights where source = ? and destination = ?', (source, destination))
            # rows = flights.fetchall()
            # return render_template("flights.html", rows = rows)
        except:
            msg = f"No flights available to {destination} on {departure_d}. Please try another date."
            return render_template('flights.html', msg= msg)
    return render_template("flights.html")

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    with sqlite3.connect('tour.db') as db:
        dest_details = db.execute("select estimated_cost from destinations inner join users on users.username=destinations.username and users.username = ? and users.email = ?", (session['username'], session['email']))
        dest_row = dest_details.fetchall()
        hotel_details = db.execute("select cost from hotels inner join users on users.username=hotels.username and users.username = ? and users.email = ?", (session['username'], session['email']))
        hotel_row = hotel_details.fetchall()
        # flight_details = db.execute("select * from flights where username = ?", (session['username']))
        # flight_row = flight_details.fetchall()
        for i in dest_row:
            dest_pack = i[0]
        for j in hotel_row:
            hotel_pack = j[0]
        # for k in flight_row:
        #     pass
        with sqlite3.connect('tour.db') as db:
            dest_details = db.execute("select * from destinations inner join users on users.username=destinations.username and users.username = ? and users.email = ?", (session['username'], session['email']))
            dest_row = dest_details.fetchall()
            hotel_details = db.execute("select * from hotels inner join users on users.username=hotels.username and users.username = ? and users.email = ?", (session['username'], session['email']))
            hotel_row = hotel_details.fetchall()
            flight_details = db.execute("select * from flights inner join users on users.username=flights.username and users.username = ? and users.email = ?", (session['username'], session['email']))
            flight_row = flight_details.fetchall()
            for i in dest_row:
                package_name = i[2]
                place = i[3]
                no_of_days = i[4]
                booking_date = i[5]

            for j in hotel_row:
                category = j[3]   
                room_type = j[4]
                no_of_guests = j[5]
                check_in_date = j[6]
                check_out_date = j[7]
                no_of_days = j[8]

            for k in flight_row:
                trip_type = k[2]
                class_type = k[3]
                departure_d = k[4]
                return_d = k[5]
                passengers = k[6]
                source = k[7]
                destination = k[8]
            try:
                db.execute("insert into bookings values(null, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(session['name'], session['email'], passengers, package_name, place, no_of_days, booking_date, category, room_type, no_of_guests, check_in_date, check_out_date, trip_type, class_type, departure_d, return_d, source, destination, session['username']))
                db.commit()
            except:
                msg = "Something went wrong while booking!"
                return render_template("payment.html", msg = msg)
        total_amount = int(dest_pack) + int(hotel_pack)
    if request.method == "POST":
        return redirect(url_for('bookingdetails'))
    if request.method == "GET":
        return render_template("payment.html", total_amount = total_amount)
        
    return render_template("payment.html")

@app.route('/bookings', methods=['GET', 'POST'])
def bookingdetails():
    if request.method == "GET":
        with sqlite3.connect('tour.db') as db:
            try:
                db.row_factory = sqlite3.Row
                cur = db.cursor()
                cur.execute("select * from bookings inner join users on users.username=bookings.username and users.username = ? and users.email = ?", (session['username'], session['email']))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                return render_template("bookings.html", rows=rows)
            except:
                msg = "No Bookings yet!"
                return render_template("bookings.html", msg = msg)
        # cur = db.cursor()
        # cur.execute("SELECT * FROM bookings where username = ?", (session['username']))
        # rows = cur.fetchall()
        # return render_template("bookings.html", rows = rows)
    return render_template("home.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")    


@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(port=5665, debug=True)