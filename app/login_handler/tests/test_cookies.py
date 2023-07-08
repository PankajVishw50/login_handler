from login_handler import config_settings
from login_handler import helpers
from login_handler import data

from .utils import SESSION_COOKIE_NAME
from .utils import LOGIN_PAGE_PATH


class TestConfigSettings(object):
    """Tests if changing settings are working
    
    """
    
    def test_httponly(self, app, reset):
        config_settings(httponly=False)

        assert app.login_handler.HTTPONLY is False

    def test_samesite(self, app, reset):
        #: Checks default value it should be "Lax"
        assert "lax" == app.login_handler.SAMESITE.lower()

        config_settings(samesite="Strict")
        assert "strict" == app.login_handler.SAMESITE.lower()

        #: In order to check for samesite with None value
        #: We have to also define secure to True
        config_settings(samesite=None, secure=True)
        assert None is app.login_handler.SAMESITE

    def test_samesite_pairs(self, app, reset):
        #: It should throw error
        error = False
        try:
            config_settings(secure=False, samesite=None)
        except Exception as e:
            error = True
        assert error is True

        #: No error
        error = False
        try:
            config_settings(secure=True, samesite=None)
        except Exception as e:
            error = True
        assert error is False

        #: samesite = "Lax"
        #: No error
        error = False
        try:
            config_settings(secure=False, samesite="Lax")
        except Exception as e:
            error = True
        assert error is False

        #: No error
        error = False
        try:
            config_settings(secure=True, samesite="Lax")
        except Exception as e:
            error = True
        assert error is False

        #: samesite = "Strict"
        #: No error
        error = False
        try:
            config_settings(secure=False, samesite="Strict")
        except Exception as e:
            error = True
        assert error is False

        #: No error
        error = False
        try:
            config_settings(secure=True, samesite="Strict")
        except Exception as e:
            error = True
        assert error is False

    def test_remember(self, app, reset):
        #: Checks default value
        assert app.login_handler.REMEMBER is False

        config_settings(remember=True)
        assert app.login_handler.REMEMBER is True

    def test_unaccessed_timeout(self, app, reset):
        ninety_three_days_in_seconds = (60*60*24) * 93
        config_settings(unaccessed_timeout=ninety_three_days_in_seconds)

        assert ninety_three_days_in_seconds == app.login_handler.UNACCESSED_TIMEOUT

    def test_accessed_timeout(self, app, reset):
        sixty_nine_days_in_seconds = (60*60*24) * 63
        config_settings(accessed_timeout=sixty_nine_days_in_seconds)

        assert sixty_nine_days_in_seconds == app.login_handler.ACCESSED_TIMEOUT

    def test_domain(self, app, reset):
        assert app.login_handler.DOMAIN is None

        config_settings(domain="example")
        assert "example" == app.login_handler.DOMAIN

    def test_path(self, app, reset):
        assert app.login_handler.PATH == "/"

        config_settings(path="/test")
        assert "/test" == app.login_handler.PATH


class TestCookies(object):
    username = "ritik"
    password = "rit"
    session_cookie_name = SESSION_COOKIE_NAME

    def test_httponly_default(self, app, client, reset):
        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        #: Checks all default values
        assert app.login_handler.HTTPONLY == client.get_cookie(self.session_cookie_name).http_only
        assert app.login_handler.SAMESITE == client.get_cookie(self.session_cookie_name).same_site
        assert app.login_handler.PATH == client.get_cookie(self.session_cookie_name).path
        assert app.login_handler.SECURE == client.get_cookie(self.session_cookie_name).secure
        assert app.login_handler.DOMAIN is None

    def test_httponly_false(self, app, client, reset):
        config_settings(httponly=False)

        #: Check if default values changes to False
        assert app.login_handler.HTTPONLY is False

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        }, follow_redirects=True)

        #: check httponly with all values
        assert app.login_handler.HTTPONLY == client.get_cookie(self.session_cookie_name).http_only

        assert app.login_handler.SAMESITE == client.get_cookie(self.session_cookie_name).same_site
        assert app.login_handler.PATH == client.get_cookie(self.session_cookie_name).path
        assert app.login_handler.SECURE == client.get_cookie(self.session_cookie_name).secure
        assert app.login_handler.DOMAIN is None

    def test_path(self, app, client, reset):
        #: Changing path of cookies
        config_settings(path="/dashboard")

        response = client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        }, follow_redirects=True)

        #: If everything goes right, cookies should not be sent and
        #: user should not be logged in.
        assert "Guest" in response.data.decode()

        #: Now while sending on path '/dashboard/...'
        #: cookies should work fine
        response_2 = client.get("/dashboard/check")
        assert self.username in response_2.data.decode()

    def test_domain(self, app, client, reset):
        #: It will change domain of cookies
        config_settings(domain="example")

        response = client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        }, follow_redirects=True)

        #: We do have stored valid login session cookies on browser/client
        #: But due to different domain browser/client should not send them back
        #: Hence authentication of user will not work
        assert "Guest" in response.data.decode()

    def test_samesite_default(self, app, client, reset):
        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        #: By default same_site of cookie should be "lax"
        assert "lax" == client.get_cookie(SESSION_COOKIE_NAME).same_site.lower()

    def test_samesite_strict(self, app, client, reset):
        config_settings(samesite="Strict")

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert "strict" == client.get_cookie(SESSION_COOKIE_NAME).same_site.lower()

    def test_samesite_none(self, app, client, reset):
        config_settings(samesite=None, secure=True)

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert client.get_cookie(SESSION_COOKIE_NAME).same_site is None

    def test_unaccessed_timeout_default(self, app, client, reset):
        #: remember needs to be True
        config_settings(remember=True)

        #: Creates formatted date string of current date
        default_timeout = app.login_handler.UNACCESSED_TIMEOUT
        default_timeout_in_format = helpers.get_time_from_seconds(default_timeout)

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert client.get_cookie(SESSION_COOKIE_NAME).expires.strftime(app.login_handler.time_format) == default_timeout_in_format

    def test_unaccessed_timeout_custom(self, app, client, reset):
        sixty_three_days_in_seconds = (60*60*24) * 63
        sixty_three_days_from_now_in_format = helpers.get_time_from_seconds(sixty_three_days_in_seconds)

        config_settings(unaccessed_timeout=sixty_three_days_in_seconds, remember=True)

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert client.get_cookie(SESSION_COOKIE_NAME).expires.strftime(app.login_handler.time_format) == sixty_three_days_from_now_in_format

    def test_accessed_timeout_default(self, app, client, reset):
        config_settings(remember=True)

        default_timeout = app.login_handler.ACCESSED_TIMEOUT
        default_timeout_in_format = helpers.get_time_from_seconds(default_timeout)

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert data.session.get("_accessed-timeout") == default_timeout_in_format

    def test_accessed_timeout_custom(self, app, client, reset):
        ninety_three_days_in_seconds = (60*60*24) * 93
        ninety_three_days_in_seconds_in_format = helpers.get_time_from_seconds(ninety_three_days_in_seconds)

        config_settings(accessed_timeout=ninety_three_days_in_seconds, remember=True)

        client.post(LOGIN_PAGE_PATH, data={
            "username": self.username,
            "password": self.password
        })

        assert data.session.get("_accessed-timeout") == ninety_three_days_in_seconds_in_format


