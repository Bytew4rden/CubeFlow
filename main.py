from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
import bcrypt 

app = Flask(__name__)
app.secret_key = 'Lily_Eats_Birds'
database = 'cubeflow.db'

createUsersTableQuery = """
CREATE TABLE IF NOT EXISTS users
(
user_id INTEGER PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);
"""

createSolvesTableQuery = """
CREATE TABLE IF NOT EXISTS solves
(
solve_id INTEGER PRIMARY KEY AUTOINCREMENT,
time_seconds REAL NOT NULL,
scramble TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id) 
);
"""

conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute(createUsersTableQuery)
cur.execute(createSolvesTableQuery)
conn.close()

# Auth "Blueprint" Routes #
@app.route("/")
def landing():
    if session.get("logged_in") == True:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get('un')
        password = request.form.get('pw')

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        query = "SELECT username, password FROM users WHERE username = ?"
        cur.execute(query,(username,))

        result = cur.fetchone()

        if result:
            password_bytes = password.encode('utf-8')
            hashed = result[1]

            if bcrypt.checkpw(password_bytes,hashed):

                print("password accepted")
                session["logged_in"] = True

                return redirect(url_for('home'))
            else:
                return render_template('login.html')

        else:
            return render_template('login.html')


    return render_template('login.html')

@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":
        username = request.form.get('un')
        password = request.form.get('pw')

        #Check if account exists already
        query = 'SELECT username FROM users WHERE username = ?'
        conn=sqlite3.connect(database)
        cur=conn.cursor()
        cur.execute(query,(username,))
        result = cur.fetchone()
        
        #If an account with that username exists already, return the registration page again
        # If not, your account is added to the DB, and you get taken to the login page.
        if result:
            conn.close()
            return render_template('register.html')
        else:
            password_bytes = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes,bcrypt.gensalt())
            query = 'INSERT INTO users(username,password) VALUES (?,?)'
            cur.execute(query,(username, hashed_password))
            conn.commit()
            conn.close()
            print("account made")
            return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route("/home")
def home():
    if session.get("logged_in") == True:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    
@app.route("/solve",methods=["GET","POST"])
def solve():
    if request.method == "POST":
        print("posted to /solve")
        return "<h1>posted to /solve</h1>"
    else:
        print("get from /solve")
        return "<h1>get from /solve</h1>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')