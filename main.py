from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

database = sqlite3.connect('site.db')

cursor = database.cursor()

command1="""CREATE TABLE IF NOT EXISTS
Users(user_id INTEGER PRIMARY KEY, )"""

# Routes #
@app.route("/",methods=["GET","POST"])
def home():
    print("Connected user not logged in, redirecting to login page.")
    return redirect(url_for('login'))

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route("/createacct",methods=["GET","POST"])
def createacct():
    print("rendering account creation page")
    return render_template('createaccount.html')
if __name__ == '__main__':
    app.run(debug=True)