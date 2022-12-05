from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if current_user.role == 'lecturer':
            note = request.form.get('note')

            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        else:
            from sqlalchemy.orm import sessionmaker
            from . import DB_NAME
            Session = sessionmaker(bind=f'sqlite:///{DB_NAME}')
            session = Session()
            return redirect('https://itb-ac-id.zoom.us/j/93148476230?pwd=QzFQL2h2dHB3OWtWRFZjU3JkRW5lZz09')
    if current_user.role == 'lecturer':
        return render_template("course.html", user=current_user)
    else:
        return render_template("scourse.html", user=current_user)

    


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    if request.method == 'POST':
        redirect('google.com')

    return render_template("scourse.html", user=current_user)

