from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:Patelmd%4042400@localhost:5432/notebook"
app.config["SECRET_KEY"]="mynotebook"

db = SQLAlchemy(app)

from app.auth.controllers import auth_blueprint
from app.md.controllers import md_blueprint

app.register_blueprint(auth_blueprint,url_prefix=f"/api/{auth_blueprint.url_prefix}")
app.register_blueprint(md_blueprint,url_prefix=f"/api/{md_blueprint.url_prefix}")