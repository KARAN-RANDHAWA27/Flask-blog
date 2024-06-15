from flask import Blueprint, render_template, request, redirect, url_for,flash
from flask_login import login_required, current_user
from .models import Notes
from project.db import db

views = Blueprint('views',__name__)


@views.route('/home',methods=['GET','POST','PUT'])
@login_required
def homepage():
    userNotes = Notes.query.filter_by(user_id = current_user.id).all()
    print(userNotes)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_note = Notes(title=title,data=content,user_id=current_user.id)
        try:
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully", category='success')
            return redirect(url_for('views.homepage'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating note: {str(e)}")

    elif request.method == 'PUT':
        note_id = request.args.get('note_id')
        if note_id:
            try:
                noteInstance = Notes.query.filter_by(id = int(request.args.get('note_id')), user_id = current_user.id).first()
                if noteInstance:
                    data = request.get_json()
                    title = data.get('title')
                    content = data.get('content')
                    noteInstance.title = title
                    noteInstance.data =  content
                    print('------------------------')
                    print(noteInstance)
                    db.session.commit()
                    print("huuuu")
                    flash("Note updated successfully", category='success')
                    return redirect(url_for('views.homepage'))
                else:
                    flash("Note updated successfully", category='success')
            except Exception as e:
                db.session.rollback()
                print(f"Error updating note: {str(e)}")
    return render_template("home.html",user = current_user, notes = userNotes)
