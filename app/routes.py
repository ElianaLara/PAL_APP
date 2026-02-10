from flask import render_template, redirect, url_for, session, Blueprint, flash, request
from .models import Tutor
from app.forms import LoginForm

main = Blueprint("main", __name__)


@main.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        tutor = Tutor.query.filter_by(email=form.email.data).first()

        if tutor and tutor.password_hash == form.password.data:
            session['tutor_id'] = tutor.id
            session['tutor_name'] = tutor.full_name

            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))

        flash("Invalid email or password", "danger")

    return render_template('login.html', form=form)