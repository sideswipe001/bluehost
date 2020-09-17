from flask import Flask, render_template, redirect, url_for, request, jsonify
from classes import ProductForm
import os
import csv
from io import StringIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re


SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    customer = db.Column(db.String(50))
    domain = db.Column(db.String(50))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)


db.create_all()


def validate(data):
    if data['product_type'] in ['domain', 'pdomain', 'edomain']:
        existing = Product.query.filter_by(type=data['product_type'], domain=data['domain']).first()
        if existing: # Do we have this domain registered
            return False
        if not re.match('(\w+\.\w+)$', data['domain']): # Is it top level domain
            return False
        if data['product_type'] == 'edomain': # does it end in edu if it is edomain
            if not data['domain'].endswith('.edu'):
                return False
        else: # does it end with org or com
            if not data['domain'].endswith('.org') and not data['domain'].endswith('.com'):
                return False
    if data['product_type'] in ['hosting', 'email']:
        existing = Product.query.filter_by(type=data['product_type'], domain=data['domain']).first()
        if existing: # Do we have this already
            return False
        existing = Product.query.filter(Product.type.in_(('domain', 'pdomain', 'edomain')), Product.domain == data['domain']).first()
        if not existing: # Does this have a registered domain
            return False

    if not data['duration'].isdigit(): # Is the duration a positive integer
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        form = request.form
        data = {'customer_id': form['customer_id'],
                'product_type': form['product_type'],
                'domain': form['domain'],
                'duration': form['duration']}
        if validate(data):

            bill_customer(data)
            if form['product_type'] in ['domain', 'edomain', 'pdomain']:
                register_domain(data)

            if form['product_type'] in ['pdomain']:
                secure_domain(data)

            if form['product_type'] in ['hosting']:
                provision_account(data)
                send_welcome_email(data)

            if form['product_type'] in ['email']:
                create_email_routing(data)

            new = Product(customer=form['customer_id'], type=form['product_type'], domain=form['domain'],
                          duration=form['duration'])
            db.session.add(new)
            db.session.commit()
    form = ProductForm()
    return render_template('main.html', form=form)


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    for line in csv.reader(StringIO(f.read().decode())):
        customer_id, product_type, domain, start_date, duration = line
        data = {
            'customer_id': customer_id,
            'product_type': product_type,
            'domain': domain,
            'start_date': start_date,
            'duration': duration
        }
        if validate(data):
            new = Product(customer=customer_id, type=product_type, domain=domain,
                          start_date=datetime.strptime(start_date, '%Y-%m-%d'), duration=duration)
            db.session.add(new)
            db.session.commit()

    return redirect('/')


@app.route('/list', methods=['GET'])
def list_products():
    products = []
    for product in Product.query.order_by(Product.customer).all():
        prod = product.__dict__
        del prod['_sa_instance_state']
        products.append(prod)
    return jsonify(products)


@app.route('/email', methods=['GET'])
def list_email():
    # Need to calculate the email dates and format printing
    return jsonify([])


def bill_customer(data):
    #This is a stub for billing the customer
    pass


def register_domain(data):
    #This is a stub for registering the domain
    pass


def provision_account(data):
    #This is a stub for provisioning account
    pass


def send_welcome_email(data):
    # This is a stub for sending the welcome email
    pass


def create_email_routing(data):
    # This is a stub for creating email routing
    pass


def secure_domain(data):
    # This is a stub for securing the domain
    pass


if __name__ == '__main__':
   app.run()