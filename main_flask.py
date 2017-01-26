

import os
from flask import Flask
from flask_mwoauth import MWOAuth
from builtins import input

app = Flask(__name__)
app.secret_key = os.urandom(24)

# authenticate
from local import consumer_token, secret_token
mwoauth = MWOAuth(consumer_key=consumer_token, consumer_secret=secret_token)

app.register_blueprint(mwoauth.bp)


@app.route("/")
def index():
    return "logged in as: " + repr(mwoauth.get_current_user(False)) + "<br>" + \
           "<a href=login>login</a> / <a href=logout>logout</a>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")