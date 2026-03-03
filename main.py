from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
solves = []
login = False


@app.route("/",methods=['GET','POST'])
def postInfo():
    
    if request.method == 'POST':
        data = request.get_json()

        solve={
            "solveNumber":data["solveNumber"],
            "scramble":data["scramble"],
            "time":data["time"]
        }

        solves.append( str(solve["solveNumber"]) + ": " + solve["scramble"] + " | " + str(solve["time"]) + "s" )
        return render_template('index.html',solves=solves)
    else:
        if not login:
            return render_template('login.html')
        else:
            return render_template('index.html')

    

if __name__ == '__main__':
    app.run(debug=True)