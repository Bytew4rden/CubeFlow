from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
solves = []


@app.route("/",methods=["GET","POST"])
def home():
    
    if request.method == 'POST':
        return "<p> You posted < /p>"
    else:
        return redirect(url_for('login'))
        # else:
        #     return render_template('index.html')

@app.route("/login",methods=["GET","POST"])
def login():
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)