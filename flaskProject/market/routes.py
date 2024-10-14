from flask import current_app as app, request
from market import db
from flask import render_template, redirect, url_for, flash
from market.models import Products, User, shopping_list
from market.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

# home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# products page
@app.route('/products')
@login_required
def products_page():
    items = Products.query.limit(48).all()
    return render_template('products.html', items=items)

# allows you to search for an item
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_term = request.form.get('search')
    items = Products.query.filter(Products.name.like(f'%{search_term}%')).all()
    return render_template('products.html', items=items)

# registration page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password1.data, method='pbkdf2:sha256')
        user_to_create = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('products_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

# login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and check_password_hash(attempted_user.password, form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('products_page'))
        else:
            flash('Username and Password are incorrect! Please try again!', category='danger')

    return render_template('login.html', form=form)

# logout
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for("home_page"))


@app.route('/shopping_list')
@login_required
def shopping_list_page():
    items = current_user.shopping_list
    return render_template('shopping_list.html', items=items)

# allows you to add items into a shopping list
@app.route('/add_to_shopping_list/<int:product_id>')
@login_required
def add_to_shopping_list(product_id):
    product = Products.query.filter_by(id=product_id).first()
    current_user.shopping_list.append(product)
    db.session.commit()
    flash(f'{product.name} added to your shopping list!', category='success')
    return redirect(url_for('products_page'))

# allows you to remove items youve added into your shopping list
@app.route('/remove_from_shopping_list/<int:product_id>')
@login_required
def remove_from_shopping_list(product_id):
    product = Products.query.filter_by(id=product_id).first()
    # Directly delete all instances of the product from the association table
    db.session.execute(
        shopping_list.delete().where(
            and_(
                shopping_list.c.user_id == current_user.id,
                shopping_list.c.product_id == product.id
            )
        )
    )
    db.session.commit()
    flash(f'{product.name} removed from your shopping list!', category='info')
    return redirect(url_for('shopping_list_page'))
