from flask import render_template, redirect, url_for, session, Blueprint, flash, request

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
        # Example check (replace with DB logic)
        if form.email.data == "test@test.com" and form.password.data == "1234":
            session['user'] = form.email.data
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))

        flash("Invalid credentials", "danger")

    return render_template('login.html', form=form)