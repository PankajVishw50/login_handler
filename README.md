
# login_handler 

This module can be used to help in authentication and managing login/logout 
or sessions on the web.   
It uses session-based authentication 

## Features

- Session-based authentication using cookies
- Support for the "remember me" functionality
- Encryption and decryption of cookies for enhanced security
- Customizable cookie settings such as httponly, samesite, remember, unaccessed_timeout, accessed_timeout, domain, path, and secure
- Easy integration with Flask applications
- Ability to set up user callback functions to load user information
- Supports Fresh Login 

## Installation

To install the Flask User Authentication module, use pip:

```bash
pip install login_handler
```

## Usage

Create an instance of the LoginHandler class and initialize 
it with your Flask application

```python
app = Flask(__name__)
login_handler = LoginHandler(app)
```

(remember, you can also integrate it with flask application using 
flask factory patter)

Set up a user callback function to load user information 
based on the user ID
```python
def load_user(user_id):
    # Your code to load the user based on the user ID
    # Return the user object
    pass

login_handler.init_user_callback(load_user)
```

### Logging in User
To log in user, you have to first import login function from module 

Pass the user object that represents the logged-in user.  
The user object should have the necessary methods and attributes 
required for authentication, such as 
**get_id()** and **is_authenticated()**.

```python
from login_handler import login

@app.route("/login-user")
def login_user():
    login(user)
```

The user will only be loaded if method **is_authenticated**
returns True otherwise It will give raise error. 

This way user will only be logged in for session (default)
if not changed otherwise.

### Logging out User
To log out user, you have to first import logout function from module

In order to log out the current logged-in user, you have to call the
function without any arguments, and it will log out the current user.

```python
from login_handler import logout

@app.route("/logout-user")
def logout_user():
    logout()
```

### Remember me  

If remember is set to True, There will be 2 criteria for the expiration 
of their session

1. **accessed_timeout:**: If a user doesn't access service in defined 
time (this time will be defined with `accessed_timeout` attribute), 
their session will expire. Its value will be updated with each request.
Its value can change multiple times in 1 session.

2. **unaccessed_timeout:** On expiry of this value user have to log in fresh with their credentials 
This timeout is defined by the `UNACCESSED_TIMEOUT` attribute and 
is set only once when the session is initially created.

Both of these attributes stores seconds 
and timeout are created by adding current_time + seconds 


### Default Configurations

The module provides default configuration settings for the login system. These settings can be modified to alter the behavior of the system according to your application's requirements. Below are the default configuration settings and their descriptions:

- `HTTPONLY`: This setting controls whether cookies should be accessible only through HTTP requests. It is set to `True` by default, ensuring that cookies are not accessible to client-side scripts.

- `SAMESITE`: This setting determines the behavior of the `samesite` attribute of cookies, which controls how cookies are sent in cross-site requests. The default value is `None`, but you can choose from the following options: `STRICT`, `LAX`, or `None`.

- `REMEMBER`: If this setting is set to `True`, it enables the "Remember Me" functionality. When enabled, the session will have two criteria for expiration, as explained in the "Remember Me" section of the documentation.

- `UNACCESSED_TIMEOUT`: This setting defines the expiration time for the session if the user doesn't access the service within a certain period. It is measured in seconds and set to a default value of 5,184,000 seconds, which is equivalent to 60 days.

- `ACCESSED_TIMEOUT`: This setting determines the maximum time allowed for the client to log in from the cookie. It doesn't reset until the client uses their password to log in. Additional conditions can be set by the server. By default, it is set to 31,536,000 seconds, which is equivalent to 365 days.

- `DOMAIN`: This setting specifies the domain of the cookies. By default, it is set to `None`, which means the cookies are valid for the current domain only.

- `PATH`: This setting determines the path of the cookies. It is set to `/` by default, meaning the cookies are valid for the entire domain.

- `SECURE`: If this setting is set to `True`, the cookies will only be sent over secure HTTPS connections. By default, it is set to `False`.

Additionally, the `keys` list contains the names of specific keys used in the cookies.

These default configurations provide a starting point for the login system. You can modify these settings according to your application's needs by using the `config_settings` method of the `LoginHandler` class.

For more detailed information on each configuration setting and how to customize them, refer to the module's documentation and examples.


### Changing default configurations

You can change default configurations settings defined in "Default Configurations"
section using the `config_settings`
method of the `LoginHandler` class.

Here is an example: 

```python
    config_settings(
            httponly=False,
            samesite="lax",
            remember=True,
            unaccessed_timeout=(60*60*24)*60,   # 60 days
            accessed_timeout=(60*60*24)*15,     # 15 days
            domain=None,
            path="/",
            secure=True
    )
```

The `config_settings` method accepts several parameters to modify
the default configurations. 
It is important to note that you don't need to provide values for all 
the parameters. You can selectively provide only the configurations 
you want to change, leaving the rest with their default values.




