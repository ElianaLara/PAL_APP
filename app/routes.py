from flask import render_template, redirect, url_for, session, Blueprint, flash, request
from .models import Tutor
from app.forms import LoginForm

main = Blueprint("main", __name__)


@main.route('/')
def dashboard():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    tutor_name = session.get('tutor_name')

    return render_template('dashboard_sessions.html', tutor_name=tutor_name)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        tutor = Tutor.query.filter_by(email=form.email.data).first()

        if tutor and tutor.password_hash == form.password.data:
            session['tutor_id'] = tutor.id
            session['tutor_name'] = tutor.full_name

            flash("Logged in successfully!", "success")
            return redirect(url_for('main.sessions'))

        flash("Invalid email or password", "danger")

    return render_template('login.html', form=form)

@main.route('/materials')
def materials():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_materials.html', active_tab='materials')


@main.route('/sessions')
def sessions():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_sessions.html', active_tab='sessions')


@main.route('/students')
def students():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_students.html', active_tab='students')


@main.route('/history')
def history():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_history.html', active_tab='history')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))