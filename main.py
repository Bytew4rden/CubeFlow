from flask import Flask,render_template,request,redirect,url_for
import sqlite3
import bcrypt 

app = Flask(__name__)
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
@app.route("/",methods=["GET","POST"])
def landing():
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

        query = 'SELECT username FROM users WHERE username = ?'
        conn=sqlite3.connect(database)
        cur=conn.cursor()
        cur.execute(query,(username,))
        result = cur.fetchone()
        
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')