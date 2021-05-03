from flask_mysqldb import MySQL
import MySQLdb.cursors

# Intialize MySQL
mysql = MySQL()


def get_all_contacts(order_by='CONTACT_NAME', start=1,count=10):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM contacts ORDER BY {order_by} LIMIT %s, %s',(start,count))
        contacts = cursor.fetchall()
        cursor.execute('SELECT count(1) as count from contacts')
        number_of_pages = int(cursor.fetchone()['count']/count)+1
        return contacts, number_of_pages
    except MySQLdb.Error as e:
        raise e


def get_contact(contact_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM contacts WHERE CONTACT_NAME = %s', [contact_name])
        contact = cursor.fetchone()
        return contact
    except MySQLdb.Error as e:
        raise contact


def edit_contact(birthdate, contact_type, phone, desc, contact_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE contacts SET BIRTHDATE=%s, CONTACT_TYPE=%s, PHONE=%s, DESCR=%s WHERE CONTACT_NAME=%s',
                       (birthdate, contact_type, phone, desc, contact_name))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        raise e


def create_contact(contact_name, birthdate, contact_type, phone, desc):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contacts (CONTACT_NAME,BIRTHDATE,CONTACT_TYPE,PHONE,DESCR) VALUES (%s,%s,%s,%s,%s)',
                       (contact_name, birthdate, contact_type, phone, desc))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        raise e
