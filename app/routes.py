from flask import render_template, redirect, url_for, session, Blueprint, flash, request, current_app
from .models import Tutor, Student, Material
from werkzeug.utils import secure_filename
from app.forms import LoginForm, StudentForm, MaterialForm
from . import db
import os

main = Blueprint("main", __name__)

UPLOAD_FOLDER = 'app/static/uploads'

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
    form = MaterialForm()

    # Query all materials for the logged-in tutor
    materials = Material.query.filter_by(tutor_id=session['tutor_id']).all()

    # Render the template with the materials list
    return render_template("dashboard_materials.html", materials=materials, form=form)

@main.route("/add_material", methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        filename = None
        if form.file.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))

        new_material = Material(
            tutor_id=session['tutor_id'],
            title=form.title.data,
            material_type=form.material_type.data,
            file_path=f"uploads/{filename}" if filename else None,
            description=form.description.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash("Material added successfully!", "success")
        return redirect(url_for('main.materials'))

        # Get all materials for this tutor
    materials = Material.query.filter_by(tutor_id=session['tutor_id']).all()
    return render_template("dashboard_material.html", form=form, materials=materials)

@main.route("/delete_material/<int:material_id>", methods=['GET', 'POST'])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    if material.material_type != "link" and material.file_path:
        file_path = os.path.join(current_app.root_path, "static", material.file_path.strip())
        file_path = os.path.normpath(file_path)
        # absolute path
        print("Looking for:", file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File removed")
        else:
            print("File not found")
    else:
        print("Not a file material or no path")
    db.session.delete(material)
    db.session.commit()

    flash('Material deleted successfully!', 'success')
    return redirect(url_for('main.materials'))


@main.route('/sessions')
def sessions():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    form = StudentForm()

    return render_template('dashboard_sessions.html', active_tab='sessions', form=form)


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
        form=form
    )

@main.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('main.students'))

@main.route('/history')
def history():
    if 'tutor_id' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard_history.html', active_tab='history')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))