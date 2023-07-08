

class Guest:
    """Default class for guest type of user
    """

    def get_id(self):
        return None

    def is_authenticated(self):
        return False