from flask import Flask, render_template, request, redirect, url_for, flash
from .model import create_contact, edit_contact, get_all_contacts, get_contact, mysql
import re

app = Flask(__name__)

app.secret_key = 'some_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aramon'
app.config['MYSQL_PASSWORD'] = 'Profeazul1!'
app.config['MYSQL_DB'] = 'contact_app'
ROWS_PER_PAGE = 10

mysql.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    order_by = 'CONTACT_NAME'
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        order_by = request.form.get('order_header')
    try:
        contacts, num_of_pages = get_all_contacts(order_by,page,ROWS_PER_PAGE)
    except Exception as e:
        return render_template('error_page.html', error=e)
    return render_template('index.html', contacts=contacts, cur_page = page, pages = num_of_pages)


@app.route('/detailsContact/<string:contact_name>', methods=['GET', 'POST'])
def detailsContact(contact_name):
    try:
        contact = get_contact(contact_name)
    except Exception as e:
        return render_template('error_page.html', error=e)
    return render_template('details.html', contact=contact)


@app.route('/editContact/<string:contact_name>', methods=['GET', 'POST'])
def editContact(contact_name):
    if request.method == 'POST':
        birthdate = request.form['birthdate']
        contact_type = request.form['contact_type']
        phone = request.form['phone']
        desc = request.form['description']
        contact_name = request.form['name']
        validation_errors = validateForm(contact_name, birthdate,
                                         contact_type, desc, phone)
        if validation_errors:
            return render_template('edit.html', errors=errors, contact={})
        try:
            edit_contact(birthdate, contact_type, phone, desc, contact_name)
        except Exception as e:
            return render_template('error_page.html', error=e)
        return redirect(url_for('index'))
    try:
        contact = get_contact(contact_name)
    except Exception as e:
        return render_template('error_page.html', error=e)
    return render_template('edit.html', contact=contact)


@app.route('/createContact', methods=['GET', 'POST'])
def createContact():
    if request.method == 'POST':
        contact_name = request.form['name']
        birthdate = request.form['birthdate']
        contact_type = request.form['contact_type']
        desc = request.form['description']
        phone = request.form['phone']
        validation_errors = validateForm(contact_name, birthdate,
                                         contact_type, desc, phone)
        if validation_errors:
            return render_template('create.html', errors=errors, contact={})
        try:
            create_contact(contact_name, birthdate, contact_type, phone, desc)
        except Exception as e:
            return render_template('error_page.html', error=e)
        return redirect(url_for('index'))
    return render_template('create.html')


def validateForm(name, birthdate, contact_type, desc, phone):
    CONTACT_TYPES = ['contact_type1', 'contact_type2', 'contact_type3']
    errors = {}
    if name == '':
        errors['name'] = 'Name is required'
    elif len(name) > 100:
        errors['name'] = 'Maximum length of name is 100 characters'

    if birthdate == '':
        errors['birthdate'] = 'Birth Date is required'

    if contact_type not in CONTACT_TYPES:
        errors['contact_types'] = f'Contact type invalid, admited values are: {CONTACT_TYPE}'

    if (not re.match('\d*$', phone)) or len(phone) > 10:
        print('entro')
        errors['phone'] = 'Maximum length of phone number is 10 digits'

    return errors
