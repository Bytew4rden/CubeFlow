from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)
database = 'cubeflow.db'

createTablesQuery = """
CREATE TABLE IF NOT EXISTS users
(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);

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
cur.execute(createTablesQuery)
conn.close()

# Auth "Blueprint" Routes #
@app.route("/",methods=["GET","POST"])
def home():
    print("Connected user not logged in, redirecting to login page.")
    return redirect(url_for('login'))

@app.route("/login",methods=["GET","POST"])
def login():
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
            query = f'INSERT INTO users(username,password) VALUES ({username},{password})'
            cur.execute(query)
            conn.close()
            return 
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)