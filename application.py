from flask import Flask, render_template, request, redirect, url_for
from model import create_contact, edit_contact, get_all_contacts, get_contact, remove_contact, mysql
import re

app = Flask(__name__)

app.secret_key = 'some_secret_key'

app.config['MYSQL_HOST'] = 'alejandrorh950522.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'alejandrorh95052'
app.config['MYSQL_PASSWORD'] = 'contactForm123@'
app.config['MYSQL_DB'] = 'alejandrorh95052$contact_app'
ROWS_PER_PAGE = 10

mysql.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    order_by = 'contact_name'
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        order_by = request.form.get('order_header')
    try:
        contacts, num_of_pages = get_all_contacts(
            order_by, page, ROWS_PER_PAGE)
    except Exception as e:
        return render_template('error_page.html', error=e)
    return render_template('index.html', contacts=contacts, cur_page=page, pages=num_of_pages)


@app.route('/editContact/<int:contact_id>', methods=['GET', 'POST'])
def editContact(contact_id):
    if request.method == 'POST':
        if request.form.get('edit_action') == 'REMOVE':
            try:
                remove_contact(contact_id)
                return redirect(url_for('index'))
            except Exception as e:
                return render_template('error_page.html', error=e)
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
            edit_contact(contact_id, contact_name, birthdate,
                         contact_type, phone, desc)
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('error_page.html', error=e)
    try:
        contact = get_contact(contact_id)
        return render_template('edit.html', contact=contact)
    except Exception as e:
        return render_template('error_page.html', error=e)


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
