from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello Flask!</p>"

@app.route("/about")
def aboyt():
    return "<h1>ABOUT US</h1>"

@app.route("/odd-even/<int:num>")
def odd_even(num):
    if num%2==0:
        return f" <h1> {num} is even"
    else:
        return f" <h1> {num} is odd"

    return "<h1>ABOUT US</h1>"
app.run(debug=True)