from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    _password = db.Column(db.String())
    notes= db.relationship("Notes",backref="user", cascade="all, delete")

    @property
    def password(self):
        """Reading the plaintext password value is not possible or allowed."""
        raise AttributeError("cannot read password")
    
    @password.setter
    def password(self, password):
        """
        Intercept writes to the `password` attribute and hash the given
        password value.
        """
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        """
        Accept a password and hash the value while comparing the hashed
        value to the password hash contained in the database.
        """
        return check_password_hash(self._password, password)