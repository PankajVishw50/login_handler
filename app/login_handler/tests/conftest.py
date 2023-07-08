import pytest

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template_string

from login_handler import LoginHandler
from login_handler import login
from login_handler import logout
from login_handler import reset_settings

from .utils import LOGOUT_PAGE_PATH

#: This ``dict`` will work as a database for testing
#: Key: User id
#: db[key] = {"username":str : "", "email":str : "", "age":int : 0, "password":str : ""}
#: we will be using username as id for ease of testing
database = dict()


@pytest.fixture(scope="session")
def db():

    #: Adding some users to database
    database["ritik"] = {"username": "ritik", "email": "ritik-jangli@gmail.com", "age": 32, "password": "rit"}
    database["sehwag"] = {"username": "sehwag", "email": "sehwag.kuli@gmail.com", "age": 32, "password": "seh"}
    database["sakshi"] = {"username": "sakshi", "email": "sakshiladyboy@gmail.com", "age": 32, "password": "sak"}

    return database


@pytest.fixture(scope="session")
def app(db):
    application = Flask(__name__)

    application.config["TESTING"] = True
    application.secret_key = "kfjwelkfjwoepfjwoeifjlwekj"

    login_handler = LoginHandler(application)

    login_handler.init_user_callback(user_callback_function)

    @application.route("/")
    def index():
        text = """
        <h1> Index Page </h1>
        
        {% if user.is_authenticated() %}
            Hello, {{ user.username }}
        {% else %}
            Hello, Guest
        {% endif %}
        """

        return render_template_string(text)

    @application.post("/create-user")
    def create_user():
        _username = request.form.get("username")
        _email = request.form.get("email")
        _age = request.form.get("age")
        _password = request.form.get("password")

        if _username and _email and _age and _password:
            #: checks if user already exists
            if _username in db.keys():
                return "User already exists. try with  another credentials"

            #: Creating new user
            db[_username] = {"username": _username, "email": _email, "age": int(_age), "password": _password}

            return redirect("/")

        return Exception("Invalid request")

    @application.post("/login-user")
    def login_user():
        response = make_response("")

        _username = request.form.get("username")
        _password = request.form.get("password")

        if _username and _password:
            if _username in db.keys() and db[_username]["password"] == _password:
                user = User(db[_username]["username"], db[_username]["email"], db[_username]["age"],
                            db[_username]["password"])
                login(user)

            return redirect("/")

        response.status_code = 401
        return response

    @application.get("/logout-user")
    def logout_user():
        logout()

        return "Successfully Logged out"

    @application.get("/dashboard/check")
    def dashboard_check():
        return render_template_string("I'm {{ user.username }} <br> <b>INFO</b>: {{ user.email }}, {{ user.age }}")

    with application.app_context() as context_app:
        yield application


@pytest.fixture(scope="function")
def client(app):
    with app.test_client(use_cookies=True) as client:
        yield client


@pytest.fixture(scope="function")
def reset(app, client):
    """Resets all settings and configs of login_handler and
    logs out user

    :param app: Flask app
    :param client: Client object for testing
    """
    reset_settings()
    client.post(LOGOUT_PAGE_PATH)


class User:
    """It will be used to store data of user
    ``login_handler`` needs user in object

    """

    def __init__(self, name, email, age, password):
        self.username = name
        self.email = email
        self.age = age
        self.password = password

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return True


def user_callback_function(user_id):
    """Loads user from provide string of user_id
    This function will be used by login_handler as a user loader
    It is must for login_handler to work


    :param user_id:
    :return: An instance of :class:`User` which represents a custom data structure of user
    """
    user = User(database[user_id]["username"], database[user_id]["email"], database[user_id]["age"], database[user_id]["password"])
    return user