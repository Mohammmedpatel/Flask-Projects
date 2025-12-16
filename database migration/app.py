from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:Patelmd%4042400@localhost/users"
db=SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=True)
