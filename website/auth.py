from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    context = {"username":"", "password":""}
    if request.method == "POST":
        username = request.form['username'].replace(" ", "")
        password = request.form['password']
        pwd_hash = generate_password_hash(password)
        context = {"username":username, "password":password}
        if len(username) < 3:
            flash("This username is too short", 'danger')
            return redirect(url_for('auth.signup', context=context))
        if len(username) > 26:
            flash("The username is too long", 'danger')
            return redirect(url_for('auth.signup', context=context))
        if User.query.filter_by(username=username).first():
            flash("Some one else has taken that name", 'danger')
            return redirect(url_for('auth.signup'), context=context)
        user = User(password=pwd_hash, username=username)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("views.chat"))
    return render_template("signup.html", context_data=context)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login(user)
                return redirect(url_for("views.chat"))
        flash("Incorrect details", "danger")
        return redirect(request.referrer)
    return render_template("login.html")

@auth.route('/avail_username', methods=['GET'])
def username_available():
    user = User.query.filter_by(username=request.args["name"]).first()
    return jsonify(user != None)