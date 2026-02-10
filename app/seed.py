from datetime import date
from app import create_app, db
from app.models import Tutor, Student, Session, Material, Vocabulary

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Tutor
    tutor = Tutor(
        email="pal.tutor@ncl.ac.uk",
        password_hash="password123",
        full_name="Eliana Lara"
    )
    db.session.add(tutor)
    db.session.commit()

    # Students
    student1 = Student(
        full_name="James Wilson",
        level="A2",
        notes="Needs help with verb conjugations",
        information = "Second year Biology"
    )

    student2 = Student(
        full_name="Sofia Martinez",
        level="A-Level",
        notes="Confident speaker, needs grammar practice",
        information="Second year Chemestry"
    )

    db.session.add_all([student1, student2])
    db.session.commit()


    # Vocabulary
    vocab1 = Vocabulary(
        term="Hablar",
        meaning="To speak",
        category="verb"
    )

    vocab2 = Vocabulary(
        term="Desayuno",
        meaning="Breakfast",
        category="vocab"
    )

    db.session.add_all([vocab1, vocab2])
    db.session.commit()

    # Sessions
    session1 = Session(
        tutor_id=tutor.id,
        student_id=student1.id,
        session_type="1-1",
        date=date(2026, 2, 5),
        notes="Present tense practice and daily routine vocab"
    )

    session1.vocabularies.extend([vocab1, vocab2])

    db.session.add(session1)
    db.session.commit()

    print("Database seeded successfully")
