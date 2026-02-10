from . import db

session_materials = db.Table(
    "session_materials",
    db.Column("session_id", db.Integer, db.ForeignKey("session.id")),
    db.Column("material_id", db.Integer, db.ForeignKey("material.id"))
)

session_vocabularies = db.Table(
    "session_vocabularies",
    db.Column("session_id", db.Integer, db.ForeignKey("session.id")),
    db.Column("vocabulary_id", db.Integer, db.ForeignKey("vocabulary.id"))
)

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    students = db.relationship("Student", backref="tutor")
    full_name = db.Column(db.String(100))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"))
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    level = db.Column(db.String(50))  # GCSE, A-level, Beginner, etc
    notes = db.Column(db.Text)

    information =db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.now())

    sessions = db.relationship("Session", backref="student", lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    session_type = db.Column(db.String(20))
    # "group" or "1-1"

    date = db.Column(db.Date, nullable=False)

    notes = db.Column(db.Text)

    materials = db.relationship("Material", secondary="session_materials")
    vocabularies = db.relationship("Vocabulary", secondary="session_vocabularies")

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"))

    title = db.Column(db.String(100), nullable=False)
    material_type = db.Column(db.String(50))
    # pdf, video, ppt, link

    file_path = db.Column(db.String(255))
    # where the file is stored

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    term = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(255))
    category = db.Column(db.String(50))
    # grammar, vocab, phrase

