import datetime


def verify_user(user):
    """It validates if user object is valid/compatible

    User object should have

    :param user: user object should have the following methods to be validated:
                - get_id : returns id as string
                - is_authenticated : returns boolean value


    :return: True if the user object is valid, otherwise returns an exception with an error message.
    """
    try:
        _id = user.get_id()

        if not isinstance(_id, str):
            return Exception("Invalid return from get_id")

    except Exception as e:
        return Exception(e)

    try:
        _verify = user.is_authenticated()

        if not isinstance(_verify, bool):
            return Exception("Invalid return from is_authenticated")

    except Exception as e:
        return Exception(e)

    return True


def get_time_from_seconds(seconds):
    cur = datetime.datetime.now()
    after_seconds = datetime.timedelta(seconds=seconds)
    then = cur + after_seconds
    return then.strftime("%d %b %Y")









