from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
import rsa 
import json

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapp'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()

    return render_template("index.html", employees = data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        gender = request.form['gender']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (name, email, phone, age, gender) VALUES (%s, %s, %s, %s, %s)", (name, email, phone, age, gender))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for("Index"))

@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        gender = request.form['gender']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE employees SET name=%s, email=%s, phone=%s, age=%s, gender=%s
        WHERE id=%s
        """, (name, email, phone, age, gender, id_data))
        flash("Data Update Successfully")
        return redirect(url_for('Index')) 


@app.route('/chart', methods=['POST', 'GET'])
def chart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT GENDER from employees GROUP BY GENDER")
    d2 = cur.fetchall()
    cur.execute("SELECT count(GENDER) from employees GROUP BY GENDER")
    d1 = cur.fetchall()
    cur.execute("SELECT DISTINCT age from employees GROUP BY age")
    d3 = cur.fetchall()
    cur.execute("SELECT count(age) from employees GROUP BY age")
    d4 = cur.fetchall()
    cur.execute("SELECT name from employees ORDER BY name ASC")
    d5 = cur.fetchall()
    cur.close()
    d1 = json.dumps(d1)
    d2 = json.dumps(d2)
    d3 = json.dumps(d3)
    d4 = json.dumps(d4)
    return render_template("chart.html", GENDER=d1, Glabel=d2, age=d4, alabel=d3)



def encryptFernet(message):
    global key
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    print("original string: ", message)
    print("encrypted string: ", encMessage)
    return encMessage



def decryptFernet(message):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message).decode()
    print("decrypted string: ", decMessage)
    return decMessage

@app.route('/encrsa', methods=['POST', 'GET'])
def encryptRSA():

    publicKey, privateKey = rsa.newkeys(512)
    message = "hello geeks"
    encMessage = rsa.encrypt(message.encode(),publicKey)

    print("original string: ", message)
    print("encrypted string: ", encMessage)
    decMessage = rsa.decrypt(encMessage, privateKey).decode()

    print("decrypted string: ", decMessage)
    return decMessage


if __name__ == "__main__":
    app.run(debug=True)

