from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import bcrypt
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")
app = Flask(__name__)

app.secret_key = config["secret_key"]
database = "cubeflow.db"

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
solve_id INTEGER PRIMARY KEY,
scramble TEXT,
time_seconds REAL NOT NULL,
penalty TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id) 
);
"""

conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute(createUsersTableQuery)
cur.execute(createSolvesTableQuery)
conn.commit()
conn.close()


# Auth "Blueprint" Routes #
@app.route("/")
def landing():
    if session.get("logged_in") == True:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        return render_template("index.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("un")
        password = request.form.get("pw")

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        query = "SELECT user_id, username, password FROM users WHERE username = ?"
        cur.execute(query, (username,))

        result = cur.fetchone()

        if result:
            password_bytes = password.encode("utf-8")
            hashed = result[2]

            if bcrypt.checkpw(password_bytes, hashed):

                session["user_id"] = result[0]
                session["logged_in"] = True
                print(f"password accepted: User #{session["user_id"]}")
                conn.close()
                return redirect(url_for("landing"))
            else:
                conn.close()
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("un")
        password = request.form.get("pw")

        # Check if account exists already
        query = "SELECT username FROM users WHERE username = ?"
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(query, (username,))
        result = cur.fetchone()

        # If an account with that username exists already, return the registration page again
        # If not, your account is added to the DB, and you get taken to the login page.
        if result:
            conn.close()
            return render_template("register.html")
        else:
            password_bytes = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            query = "INSERT INTO users(username,password) VALUES (?,?)"
            cur.execute(query, (username, hashed_password))
            conn.commit()
            conn.close()
            print("account made")
            return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route("/solve", methods=["GET", "POST"])
def solve():
    if request.method == "POST":
        # Upload solve into DB
        query = """
        INSERT INTO solves(time_seconds,scramble,user_id) VALUES (?,?,?)
        """
        solveData = request.get_json()
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(
            query,
            (
                solveData["time"],
                solveData["scramble"],
                session["user_id"],
            ),
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Solve recorded"}), 200
    else:
        print("get from /solve")
        return "<h1>get from /solve</h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
