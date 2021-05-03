from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'some_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aramon'
app.config['MYSQL_PASSWORD'] = 'Profeazul1!'
app.config['MYSQL_DB'] = 'contact_app'

# Intialize MySQL
mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    column = 'CONTACT_NAME'
    if request.method == 'POST':
        column = request.form.get('order_header')
    query = f'SELECT * FROM contacts ORDER BY {column}'
    print(query)
    cursor.execute(query)
    contacts = cursor.fetchall()
    return render_template('index.html', contacts=contacts)


@app.route('/detailsContact/<string:contact_name>', methods=['GET', 'POST'])
def detailsContact(contact_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM contacts WHERE CONTACT_NAME = %s', [contact_name])
    contact = cursor.fetchone()
    return render_template('details.html', contact=contact)


@app.route('/editContact/<string:contact_name>', methods=['GET', 'POST'])
def editContact(contact_name):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM contacts WHERE CONTACT_NAME = %s', [contact_name])
        contact = cursor.fetchone()
        return render_template('edit.html', contact=contact)
    else:
        contact_name = request.form['name']
        birthdate = request.form['birthdate']
        contact_type = request.form['contact_type']
        desc = request.form['description']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE contacts SET BIRTHDATE=%s, CONTACT_TYPE=%s, PHONE=%s, DESCR=%s WHERE CONTACT_NAME=%s',
                       (birthdate, contact_type, phone, desc, contact_name))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/createContact', methods=['GET', 'POST'])
def createContact():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        contact_name = request.form['name']
        birthdate = request.form['birthdate']
        contact_type = request.form['contact_type']
        desc = request.form['description']
        phone = request.form['phone']
        print(len(desc), 'aaaaa')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contacts (CONTACT_NAME,BIRTHDATE,CONTACT_TYPE,PHONE,DESCR) VALUES (%s,%s,%s,%s,%s)',
                       (contact_name, birthdate, contact_type, phone, desc))
        mysql.connection.commit()
        return redirect(url_for('index'))
