from flask import (
    Flask,
    render_template,
    request,
    Response,
    redirect,
    url_for,
    session,
    jsonify,
    flash,
)
import sqlite3
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
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
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
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
                    session.permanent = False
                    conn.close()
                    return redirect(url_for("landing"))
                else:
                    conn.close()
                    return redirect(url_for("login"))
            else:
                conn.close()
                return redirect(url_for("login"))
        except Exception:
            return jsonify(error="Internal Server Error")
    else:
        if session.get("logged_in") == True:
            return redirect(url_for("landing"))
        else:
            return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        try:
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
                flash("Username taken", "un_error")
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
        except Exception:
            return jsonify(error="Internal Server Error")
    else:
        return render_template("register.html")


@app.route("/solve", methods=["POST"])
def solve():
    if request.method == "POST":
        # Upload solve into DB
        query = "INSERT INTO solves(time_seconds,scramble,user_id) VALUES (?,?,?)"
        solveData = request.get_json()

        time = solveData["time"]
        scramble = solveData["scramble"]
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Login Required"})

        conn = sqlite3.connect(database)
        cur = conn.cursor()

        try:
            cur.execute(query, (time, scramble, user_id))
            conn.commit()
            return jsonify(message="Success: Solve Recorded")
        except Exception:
            return jsonify(error="Error uploading solve to DB")
        finally:
            conn.close()


@app.route("/get_solves")
def get_solves():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Login Required"})

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        query = " SELECT * FROM solves WHERE user_id = ? ORDER BY solve_id"
        cur.execute(query, (user_id,))
        solves = [dict(solve) for solve in cur.fetchall()]
        return jsonify(solves)

    except Exception:
        return jsonify(error="Internal Server Error, could not get Solves")

    finally:
        conn.close()


@app.route("/delete_solve/<int:solveID>", methods=["DELETE"])
def delete_solve(solveID):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Login Required"})

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    try:
        query = " DELETE FROM solves WHERE user_id = ? AND solve_id = ?"
        cur.execute(query, (user_id, solveID))
        conn.commit()
        return jsonify({"message": "Solve Deleted"})
    except Exception:
        return jsonify(error="Internal Server Error, Could not delete Solve")
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
