from .utils import LOGIN_PAGE_PATH
from .utils import LOGOUT_PAGE_PATH


class TestV1(object):

    def test_login(self, client, reset):
        username = "sehwag"
        password = "seh"

        response = client.post(LOGIN_PAGE_PATH, data={
            "username": username,
            "password": password
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b"Index Page" in response.data
        assert username in response.data.decode("utf-8")

        #: We will again check with index page to check if the session is working fine
        response_2 = client.get("/")

        assert response_2.status_code == 200
        assert b"Index Page" in response_2.data
        assert username in response_2.data.decode("utf-8")

    def test_login_create_checkLastLogin_loginCurrent_1(self, app, client, reset):
        """In this test, we will check if creating a new user
        raise any issue
        """

        username = "sehwag"
        password = "seh"

        response = client.post(LOGIN_PAGE_PATH, data={
            "username": username,
            "password": password
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b"Index Page" in response.data
        assert username in response.data.decode("utf-8")


        username_2 = "kush"
        email_2 = "hard.kush.personal@gmail.com"
        age_2 = 19
        password_2 = "kus"

        #: Creating a new user
        response_2 = client.post("/create-user", data={
            "username": username_2,
            "email": email_2,
            "age": age_2,
            "password": password_2
        }, follow_redirects=True)

        #: It will check if the last user session is still valid
        assert response_2.status_code == 200
        assert b"Index Page" in response_2.data
        assert username in response_2.data.decode("utf-8")

        #: Now we will try to log in our newly created user
        response_3 = client.post(LOGIN_PAGE_PATH, data={
            "username": username_2,
            "password": password_2
        }, follow_redirects=True)

        assert response_3.status_code == 200
        assert b"Index Page" in response_3.data
        assert username_2 in response_3.data.decode("utf-8")

    def test_logout(self, client, reset):
        username = "sakshi"
        password = "sak"

        #: First Log in user
        response = client.post(LOGIN_PAGE_PATH, data={
            "username": username,
            "password": password
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b"Index Page" in response.data
        assert username in response.data.decode("utf-8")

        #: Now log out user and check
        response_2 = client.get(LOGOUT_PAGE_PATH)

        assert b"Successfully Logged out" in response_2.data

        #: We will also check by going to index page
        response_3 = client.get("/")

        assert b"Guest" in response_3.data

    def test_logout_login_create(self, client, reset):
        response = client.get(LOGOUT_PAGE_PATH)

        assert b"Successfully Logged out" in response.data

        username = "sakshi"
        password = "sak"

        response_2 = client.post(LOGIN_PAGE_PATH, data={
            "username": username,
            "password": password
        }, follow_redirects=True)

        assert response_2.status_code == 200
        assert b"Index Page" in response_2.data
        assert username in response_2.data.decode("utf-8")

        username_2 = "jitendra"
        email_2 = "jattChanga@gmail.com"
        age_2 = 39
        password_2 = "jit"

        response_3 = client.post("/create-user", data={
            "username": username_2,
            "email": email_2,
            "age": age_2,
            "password": password_2
        }, follow_redirects=True)

        #: It will check if the last user session is still valid
        assert response_3.status_code == 200
        assert b"Index Page" in response_3.data
        assert username in response_3.data.decode("utf-8")

