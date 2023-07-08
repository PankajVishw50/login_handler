from .configurations import ACCESSED_TIMEOUT
from .configurations import DOMAIN
from .configurations import HTTPONLY
from .configurations import PATH
from .configurations import REMEMBER
from .configurations import SAMESITE
from .configurations import SECURE
from .configurations import UNACCESSED_TIMEOUT

from .helpers import verify_user
from .helpers import get_time_from_seconds

from .user_types import Guest

import json
import datetime

from cipher_kit import Cipher
from flask import request


class LoginHandler:
    """LoginHandler object handles authentication for your webapp.
    It is session based and uses cookies to authenticate sessions/users.

    It supports flask factory pattern.
    It supports 'remember me' functionality and also provide you with all the
    basics configurations/settings for cookies which you can change
    with the help of :meth:'config_settings'

    It uses :mod:`cipher_kit` for handling of encryption and decryption
    of cookies. (secret_key is needed for this)

    @param app: Flask application

    """

    #: Flask application
    app = None

    #: This will be used to load user from user id
    user_callback = None

    user_id = None

    #: This variable holds latest information/details
    info = None

    #: This is used as flag
    #: It indicated server have requested for logout when True
    #: :meth:'post_request' performs logout on next response
    logout_user = False

    time_format = "%d %b %Y"

    #: Template for cookies
    cookies = {
        "_login-session": None,
        "_logout-session": {
            "_valid-session": False,
            "_user-id": None
        },
        "extra": []
    }

    #: It will store data about session
    #: and current user
    session_data = dict()

    def __init__(self, app=None):

        #: These settings are for session cookies
        #: This would be used on next cookies
        #: Check :file:`configurations.py` for more info on
        #: individual settings
        self.HTTPONLY = HTTPONLY
        self.SAMESITE = SAMESITE
        self.REMEMBER = REMEMBER
        self.UNACCESSED_TIMEOUT = UNACCESSED_TIMEOUT
        self.ACCESSED_TIMEOUT = ACCESSED_TIMEOUT
        self.DOMAIN = DOMAIN
        self.PATH = PATH
        self.SECURE = SECURE

        if app:
            self.init_app(app)

    def init_app(self, app):
        """This method helps in initializing and setting up necessary
        settings for our module to work.

        It supports flask factory pattern.

        :param app: Flask app
        """
        self.app = app

        self.app.login_handler = self
        self.app.before_request(self.pre_request)
        self.app.after_request(self.post_request)
        app.template_context_processors[None].append(lambda: dict(user=self.user))

        if not self.app.secret_key:
            raise Exception("Secret Key is not defined")

    def init_user_callback(self, user_callback_func):
        """Initialize :attr:`user_callback`
        which is necessary to load user

        :param user_callback_func:
        :return:
        """
        self.user_callback = user_callback_func

    def config_settings(
            self,
            httponly=HTTPONLY,
            samesite=SAMESITE,
            remember=REMEMBER,
            unaccessed_timeout=UNACCESSED_TIMEOUT,
            accessed_timeout=ACCESSED_TIMEOUT,
            domain=DOMAIN,
            path=PATH,
            secure=SECURE
    ):
        """

        :param httponly: If sets to True cookies will only be available in requests and responses
        :param samesite: The ``samesite`` attribute of cookies is used to control how cookies are sent by the
         browser in cross-site requests.
        :param remember: On True, will remember session for :attr:`unaccessed_timeout` time period
        :param unaccessed_timeout: It expires session after :attr:`unaccessed_timeout` until user
         login again with credentials instead of sessions
        :param accessed_timeout: Time of cookie to expire if client doesn't visit at least one time
        :param domain: Domain of cookies
        :param path: Path of cookies
        :param secure: If set's to True cookie will only be sent over secure HTTPS connections

        """
        self.HTTPONLY = httponly
        self.REMEMBER = remember
        self.UNACCESSED_TIMEOUT = unaccessed_timeout
        self.ACCESSED_TIMEOUT = accessed_timeout
        self.DOMAIN = domain
        self.PATH = path
        self.SECURE = secure

        #: Combination of (samesite=None, secure=False) is invalid.
        #: In order to samesite be None secure have to be True
        if samesite is None and self.SECURE is False:
            raise Exception(f"Invalid combination of values (samesite={samesite}, secure={secure})")

        self.SAMESITE = samesite

    def reset_settings(self):
        self.HTTPONLY = HTTPONLY
        self.SAMESITE = SAMESITE
        self.REMEMBER = REMEMBER
        self.UNACCESSED_TIMEOUT = UNACCESSED_TIMEOUT
        self.ACCESSED_TIMEOUT = ACCESSED_TIMEOUT
        self.DOMAIN = DOMAIN
        self.PATH = PATH
        self.SECURE = SECURE

    @property
    def user(self):
        if not self.user_id:
            return Guest()

        return self.user_callback(self.user_id)

    @user.setter
    def user(self, data):
        raise TypeError("Cannot set attribute.")

    @property
    def logout(self):
        return self.logout_user

    @logout.setter
    def logout(self, data):
        """Sets :attr:`logout_user` to True/False

        :param data: Boolean value
        """
        if not isinstance(data, bool):
            raise ValueError("Invalid data type")

        self.logout_user = data

    def bound_login_cookie_with_next_response(self, value):
        """Sets cookie to :attr:`cookies["_login-session"]`

        :param value: Encrypted cookie as string
        """
        self.cookies["_login-session"] = value

    def init_login(self, user):
        """Sets necessary settings, cookies to login user
        cookies will be sent with next response

        :param user: Object
        :return:
        """

        #: Checks if user is valid
        if not verify_user(user):
            raise Exception("Invalid type of user")

        #: Preparing Cookie to sent over next response
        cookie = {
            "_user-id": user.get_id(),
            "_accessed-timeout": get_time_from_seconds(self.ACCESSED_TIMEOUT),
            "_valid-session": True
        }

        #: Converting Object to json
        json_cookie = json.dumps(cookie)

        #: encrypting cookie for security purposes
        encrypted_cookie = Cipher.encrypt(json_cookie, self.app.secret_key)

        #: bounded encrypted cookies to next response
        self.bound_login_cookie_with_next_response(encrypted_cookie)

        self.user_id = user.get_id()
        self.session_data = cookie

        #: updating :attr:`info`
        self.info = "User logged in"

    def init_logout(self, response):
        """Sets necessary settings, cookies to logout user
        cookies will be sent with next response

        :param response: Flask response object
        :return: Flask response
        """

        #: converts object to json
        json_logout_session = json.dumps(self.cookies["_logout-session"])

        #: encrypts it with ``secret_key``
        encrypted_logout_session = Cipher.encrypt(json_logout_session, self.app.secret_key)

        response.set_cookie(
            key="_login-session",
            value=encrypted_logout_session,
            max_age=0,
            httponly=self.HTTPONLY,
            samesite=self.SAMESITE,
            domain=self.DOMAIN,
            path=self.PATH
        )
        self.user_id = None
        self.session_data = None

        return response

    def pre_request(self):
        """It runs each time any request comes before view function

        It checks received cookies and load user
        according to cookies data
        """

        login_session = request.cookies.get("_login-session")

        #: Loads user if
        #: cookies is present, valid and logout is not True
        if login_session and not self.logout:
            decrypted_session = Cipher.decrypt(login_session, self.app.secret_key)
            obj_session = json.loads(decrypted_session)

            #: Checks if session is valid
            if not obj_session.get("_valid-session"):
                self.user_id = None
                return

            _expiration = obj_session.get("_accessed-timeout")
            _expiration_date = datetime.datetime.strptime(_expiration, self.time_format)

            #: checks unaccessed expiry date
            if _expiration_date < datetime.datetime.now():
                self.logout = True

            _user_id = obj_session.get("_user-id")
            self.user_id = _user_id
            self.session_data = obj_session

            return
        self.user_id = None
        self.session_data = None

    def post_request(self, response):
        """It runs each time any request comes after view function

        It handles setting new cookies and checking other
        important things

        :param response:
        :return:
        """

        login_session = request.cookies.get("_login-session")

        if self.cookies["_login-session"]:
            response.set_cookie(
                key="_login-session",
                value=self.cookies["_login-session"],
                httponly=self.HTTPONLY,
                samesite=self.SAMESITE,
                domain=self.DOMAIN,
                path=self.PATH,
                max_age=self.UNACCESSED_TIMEOUT if self.REMEMBER else None,
                secure=self.SECURE
            )

            self.cookies["_login-session"] = None

        if self.logout:
            self.init_logout(response)
            self.logout = False

        return response
