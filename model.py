from flask_mysqldb import MySQL
import MySQLdb.cursors

# Intialize MySQL
mysql = MySQL()

def get_all_contacts(order_by='contact_name', start=1, count=10):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            f'SELECT * FROM contacts ORDER BY {order_by} LIMIT %s, %s', (start, count))
        contacts = cursor.fetchall()
        cursor.execute('SELECT count(1) as count from contacts')
        number_of_pages = int(cursor.fetchone()['count']/count)+1
        return contacts, number_of_pages
    except MySQLdb.Error as e:
        raise e


def get_contact(contact_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM contacts WHERE id = %s', [contact_id])
        contact = cursor.fetchone()
        return contact
    except MySQLdb.Error as e:
        raise e


def edit_contact(contact_id, contact_name, birthdate, contact_type, phone, desc):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE contacts SET contact_name=%s, birthdate=%s, contact_type=%s, phone=%s, descr=%s WHERE id = %s',
                       (contact_name, birthdate, contact_type, phone, desc, contact_id))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        raise e


def create_contact(contact_name, birthdate, contact_type, phone, desc):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contacts (contact_name,birthdate,contact_type,phone,descr) VALUES (%s,%s,%s,%s,%s)',
                       (contact_name, birthdate, contact_type, phone, desc))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        raise e


def remove_contact(contact_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM contacts WHERE id=%s', (contact_id,))
        mysql.connection.commit()
    except MySQLdb.Error as e:
        raise e
