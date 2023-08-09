from flask import Flask, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from user_conn import UserConn
from address_conn import AddressConn
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin
import os
from dotenv import load_dotenv
from find_destination import FindDestination

# Test Addresses
# 506 Starflower St Warrington, PA 18976
# 3207 hemmingway drive North Whales, PA 19454
# 550 Valley View Langhorne, PA 19047
# 563 Woodview ln Harleysville, PA 19438



load_dotenv()
API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    check_password = PasswordField("Retype Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign Up")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")


class AddressForm(FlaskForm):
    destination = StringField(label="Destination", validators=[DataRequired()])
    address_1 = StringField(label="Address 1")
    address_2 = StringField(label="Address 2")
    address_3 = StringField(label="Address 3")
    address_4 = StringField(label="Address 4")
    submit = SubmitField(label="Submit")


class SaveAddressForm(FlaskForm):
    name_save = StringField(label="Enter a name to save address group", validators=[DataRequired()])
    submit_save = SubmitField(label="Submit")


# Used to store user credentials for login session
class LoginObject(UserMixin):
    pass


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "Testing"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
USER = LoginObject()




@login_manager.user_loader
def load_user(username):
    user_conn = UserConn()
    if not user_conn.get_user(username):
        return

    user = LoginObject()
    user.id = username
    return user


@app.route("/signup", methods=["GET", "POST"])
def signup():
    user_conn = UserConn()
    username_taken = ""
    mismatch = ""
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(signup_form.password.data)
        if user_conn.get_user(signup_form.username.data):
            username_taken = "Username taken"
        elif not(signup_form.password.data == signup_form.check_password.data):
            mismatch = "Passwords don't match"
        elif signup_form.password.data == signup_form.check_password.data:
            user_conn.insert_user(signup_form.username.data, hashed_password)
            return redirect(url_for("login"))

    return render_template("SignUp.html", form=signup_form, taken=username_taken, mismatch=mismatch)


@app.route("/login", methods=["GET", "POST"])
def login():
    user_conn = UserConn()
    login_form = LoginForm()
    wrong_credentials = ""
    if login_form.validate_on_submit():
        try:
            # Get user info from database
            db_user_info = user_conn.get_user(login_form.username.data)
        except TypeError:
            pass
        else:
            if db_user_info:
                db_user_password = db_user_info[2]
                if bcrypt.check_password_hash(db_user_password, login_form.password.data):
                    USER.id = db_user_info[1]
                    session["username"] = db_user_info[0]
                    login_user(USER)

                    return redirect(url_for("home"))
                else:
                    wrong_credentials = "The username or password is incorrect"
            else:
                wrong_credentials = "The username or password is incorrect"

    return render_template("login.html", form=login_form, wrong_credentials=wrong_credentials)


@app.route("/logout", methods=['Get', "Post"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    #print(USER.get_id())
    address_conn = AddressConn()
    user_conn = UserConn()
    destination_locations = ["Empire State Building"]
    find_location = FindDestination()
    address_form = AddressForm()
    save_addresses_form = SaveAddressForm()

    if address_form.validate_on_submit():
        address_list = []
        destination = address_form.destination.data

        # clear destination list only if there is an input address
        if address_form.address_1.data or address_form.address_2.data or address_form.address_3.data or address_form.address_4.data:
            destination_locations.clear()

        # Retrieve addresses
        if address_form.address_1.data:
            address_list.append(address_form.address_1.data)
        if address_form.address_2.data:
            address_list.append(address_form.address_2.data)
        if address_form.address_3.data:
            address_list.append(address_form.address_3.data)
        if address_form.address_4.data:
            address_list.append(address_form.address_4.data)

        if len(address_list) >= 1:
            # Computations for finding the destination with the shortest average distance
            lat_long_origin_addresses = find_location.get_latitude_longitude(address_list)
            midpoint = find_location.average_latitude_longitude(lat_long_origin_addresses)
            destination_locations = find_location.find_locations(destination, midpoint)
            lat_long_dest_addresses = find_location.get_latitude_longitude(destination_locations)
            distances = find_location.calculate_distance(lat_long_origin_addresses, lat_long_dest_addresses)
            shortest_destination = find_location.shortest_distance_destination(distances)
            destination_locations[0] = shortest_destination


    if save_addresses_form.validate_on_submit():
        user_id = int(session["username"])
        name = save_addresses_form.name_save.data
        address_conn.insert_address(user_id, name, address_form.address_1.data, address_form.address_2.data,
                                    address_form.address_3.data, address_form.address_4.data)

    return render_template("Home.html", api_key=API_KEY_GOOGLE,
                           address_form=address_form, save_address_form=save_addresses_form,
                           destination=destination_locations[0])


if __name__ == "__main__":
    app.run(debug=True)



