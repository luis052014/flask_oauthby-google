from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from os import getenv
from dotenv import load_dotenv


app = Flask(__name__)

app.secret_key='mysecretkey'

oauth = OAuth(app)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
   name="google",
   client_id=getenv("CLIENT_ID"),
   client_secret=getenv('SECRET_ID'),
   server_metadata_url=CONF_URL,
   client_kwargs={
      'scope':'openid email profile'
   }
)


@app.route("/")
def main():
    return "iniciaste sesión"


@app.route("/login")
def login():
    redirect_url = url_for("auth", _external=True)
    return oauth.google.authorize_redirect(redirect_url)


@app.route("/auth")
def auth():
    token = oauth.google.authorize_access_token()
    response = oauth.google.parse_id_token(token)
    print(response)
    return redirect("/")



if __name__ == '__main__':
   load_dotenv()
   app.run(debug=True,port=4000)
