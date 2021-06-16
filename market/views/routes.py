from werkzeug.security import check_password_hash
from market import app
from market import db
from market import jwt_redis_blocklist
from flask import render_template, redirect, url_for, flash, request, session, logging, jsonify
from market.views.forms import RegisterForm, LoginForm, AddJewelryForm
from market.models.user_models import User
from market.models.item_models import Jewelry
import datetime
import uuid
import sqlite3
import os.path

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate:
        user_to_create = User(first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              email=form.email.data,
                              birth=form.birth.data,
                              phone_number=form.phone_number.data,
                              password=form.password_1.data,
                              public_id=str(uuid.uuid4()))
        db.session.add(user_to_create)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for("login"))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register_test.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # if password is matched, allow user to access and save email and first name inside the session
            flash('You have successfully logged in.', category='success')

            token = create_access_token(identity=attempted_user.public_id, expires_delta=datetime.timedelta(minutes=30))

            session['logged_in'] = True

            session['email'] = attempted_user.email

            session['first_name'] = attempted_user.first_name

            jsonify({
                'token': token,
                'user': attempted_user.public_id,
                'token_expire_to': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            })

            return redirect(url_for('index'))

        else:
            flash('Username and password are not match! Please try again!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
# @jwt_required()
def logout():
    # Removing data from session by setting logged_flag to False
    session['logged_in'] = False

    # jti = get_jwt()["jti"]
    # jwt_redis_blocklist.set(jti, "", ex=datetime.timedelta(minutes=30))
    # return jsonify(msg="Access token revoked")

    return redirect(url_for('index'))


@app.route('/add_jewelry', methods=['GET', 'POST'])
def add_jewelry():
    if session['first_name'] == 'admin':
        form = AddJewelryForm(request.form)
        if request.method == 'POST' and form.validate:
            jewelry_to_create = Jewelry(name=form.name.data,
                                  short_description=form.short_description.data,
                                  full_description=form.full_description.data,
                                  price=form.price.data,
                                  weight=form.weight.data,
                                  is_on_discount=form.is_on_discount.data,
                                  discount=form.discount.data,
                                  is_available=form.is_available.data,
                                  category_id=form.category_id.data)
            db.session.add(jewelry_to_create)
            db.session.commit()
            return render_template('success_add_jewelry.html')
        if form.errors != {}:  # If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a jewelry: {err_msg}', category='danger')
        return render_template('add_jewelry.html', form=form)
    else:
        return redirect(url_for('something_went_wrong'))


@app.route('/something_went_wrong', methods=['GET', 'POST'])
def something_went_wrong():
    return render_template('something_went_wrong.html')


def print_db():
    db_path = os.path.join("market/market.db")
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT * FROM jewelry')
        return c.fetchall()


@app.route('/all_jewelry', methods=['GET', 'POST'])
def print_all_jewelry():
    return render_template('all_jewelry.html', rows=print_db())


@app.route('/rings', methods=['GET', 'POST'])
def print_rings():
    return render_template('rings.html', rows=print_db())


@app.route('/necklaces', methods=['GET', 'POST'])
def print_necklaces():
    return render_template('necklaces.html', rows=print_db())


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    pass
