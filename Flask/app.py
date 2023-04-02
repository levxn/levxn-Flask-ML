from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from model import get_recommendations
app = Flask(__name__)
db = mysql.connector.connect(
    host="127.0.0.1", user="root", password=" ", database="login")


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("gay")
        name = request.form['text']
        mail = request.form['email']
        passw = request.form['pswd']
        cur = db.cursor()
        # Execute a query to check the credentials against the database
        query = "insert into login_tbl (username,email,password) values(%s,%s,%s)"
        values = (name, mail, passw)
        cur.execute(query, values)
        db.commit()
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form['email']
        password = request.form['pswd']
        cursor = db.cursor()
        # Execute a query to check the credentials against the database
        query = "SELECT * FROM login_tbl WHERE email= %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return redirect(url_for('model'))
        else:
            return "Invalid User"
    else:
        return render_template('login.html')


@app.route('/model', methods=['GET', 'POST'])
def model():
    if request.method == 'POST':
        genre = request.form['fname']
        genre = genre.capitalize()
        # get recommendations based on user input
        rec = get_recommendations(genre)
        return render_template('display.html', recommendations=rec)
    else:
        return render_template('model.html')


if __name__ == '__main__':
    app.run(debug=True)
