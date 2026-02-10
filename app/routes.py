from flask import render_template, redirect, url_for, session, Blueprint, flash, request
from .models import Tutor, Student
from app.forms import LoginForm, StudentForm
from . import db

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

    students = Student.query.filter_by(
        tutor_id=session['tutor_id']
    ).all()

    form = StudentForm()
    return render_template(
        'dashboard_students.html',
        students=students,
        active_tab='students',
        form = form
    )

@main.route('/add_student', methods=['GET', 'POST'])
def add_student():

    form = StudentForm()

    if form.validate_on_submit():
        new_student = Student(
            full_name=form.full_name.data,
            email=form.email.data,
            level=form.level.data,
            notes=form.notes.data,
            information=form.information.data,
            tutor_id=session['tutor_id']
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('main.students'))

    students = Student.query.filter_by(
        tutor_id=session['tutor_id']
    ).all()
    return render_template(
        'dashboard_students.html',
        students=students,
        active_tab='students',
    )

@main.route('/history')
def history():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_history.html', active_tab='history')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))