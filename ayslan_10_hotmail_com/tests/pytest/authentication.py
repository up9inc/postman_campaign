from up9lib import *

"""
This is the file to inject authentication instructions into tests.
Each test will call `authenticate()` function, passing instance of `TargetService` object into it. 
There will be made one call per service, per each test case. 
You can use `if target_key=='...'` logic when you want to have different authentication for different services. 
Look below for examples of coding authentication of different types: header, cookie, OAuth.
"""


def authenticate(target_key: str, target: TargetService):
    # Uncomment one of below lines and customize corresponding function:
    #
    # authenticate_header(target)
    # authenticate_cookie(target)
    # authenticate_oauth(target)
    if target.config_url == 'https://notify.bugsnag.com':
        pass
    elif target.config_url == 'https://www.airbnb.com.br':
        pass
    elif target.config_url == 'https://www.pousadaportela.com.br':
        pass
    else:
        pass



def authenticate_header(target: TargetService):
    # Header authentication is very simple,
    # you just need to call `target.additional_headers()`
    # and pass dictionary of headers to it.
    # These headers will be used for all API calls for corresponding service.

    token = "ABCDEF...XYZ"  # for static header value

    # token = os.environ.get("ENV_VAR")  # to load key from env variable

    # If your token is stored inside file, use below code to load it
    # with open("filename") as fp:
    #    token = fp.read()

    # set the header           <     name    >: <      value    >
    target.additional_headers({"Authorization": "Bearer " + token})
    # target.additional_headers({"X-Api-Key": token})  # any header can be set like that


def authenticate_cookie(target: TargetService):
    # All `TargetService` instances share same cookie storage
    # Just make series of requests that sets desired cookie. Like example below:

    # we request a "login form" page, if needed
    resp = target.get("/")
    resp.assert_ok()
    additional_key = resp.extract_cssselect("body form input[name='sec_key'] @value")  # taking some data from it

    # assuming this POST request will issue Set-Cookie header
    resp = target.post("/login", data={"login": "user@company.com", "password": "SecrPass", "sec_key": additional_key})
    resp.assert_ok()

    # If you have a cookie obtained somehow differently and want to add it into session storage, use this:
    merge_cookies_into_session({"name": "sessionID", "value": "21312434",
                                "path": "/", "domain": "myserver.com", "secure": True})


def authenticate_oauth(target: TargetService):
    # OAuth authentication schemas are usually implemented with a series of requests
    # Good implementation for it is available here:
    # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#web-application-flow

    client_id = r'your_client_id'
    client_secret = r'your_client_secret'
    redirect_uri = 'https://your.callback/uri'
    scope = ['scope1', 'scope2']

    from requests_oauthlib import OAuth2Session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    # ... some OAuth flow calls go here, depends on flow specifics ...

    token = oauth.fetch_token(redirect_uri)  # for example, we fetch Authorization token
    target.additional_headers({"Authorization": "Bearer " + token})

    merge_cookies_into_session(oauth.cookies)  # this is important to import cookies from OAuth, if any


