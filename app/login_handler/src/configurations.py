#: Default configurations settings for login-system 
#: You can change them to alter the behavior of the system


HTTPONLY = True

#: Set to 'lax' by default
#: Choose from These valeus - STRICT, LAX, None
SAMESITE = "Lax"

#: If sets to a True client will be remembered beyone client's session
REMEMBER = False

#: Time of cookie to expire if client doesn't visit atleast one time
#: Reset every time clients visit to site
#: Only works if REMEMBER == True
#: Default "12960000" seconds = 60 days
UNACCESSED_TIMEOUT = ((60*60) * 24) * 60

#: Max time allowed for client to login from cookie 
#: It doesn't reset once set until clients uses password to login
#: server can set additional conditions
#: Only works if REMEMBER == True
#: Default "78840000" seconds = 365 days
ACCESSED_TIMEOUT = ((60*60) * 24) * 365

#: Doesn't set domain by default
DOMAIN = None

#: By default set's to entire domain ("/")
PATH = "/"

#: If set's to True cookie only is sent over secure HTTPS connections
SECURE = False

keys = {
	"_login-session"
	"_session-id",
	"_user-id",
	"_accessed-timeout",
	"_remember",
	"_fresh-login",
	"logged_in"
	"_valid-session"
}