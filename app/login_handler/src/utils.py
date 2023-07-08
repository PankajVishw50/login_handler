from flask import current_app


def login(user):
    """Helps to Log in

    :param user: user object should have the following methods to be validated:
                - get_id : returns id as string
                - is_authenticated : returns boolean value

    """
    current_app.login_handler.init_login(user)


def logout():
    """Helps to Log out

    """
    current_app.login_handler.logout = True


def config_settings(**kwargs):
    current_app.login_handler.config_settings(**kwargs)


def reset_settings():
    current_app.login_handler.reset_settings()


class Data:
    """A class used to store data that can be accessed and utilized across the application.

    Properties:
        - user: Retrieves the current user from the login handler.
    """

    @property
    def user(self):
        return current_app.login_handler.user

    @property
    def session(self):
        return current_app.login_handler.session_data


data = Data()
