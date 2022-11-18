from flask_app import app
from flask import render_template,redirect,session,request, flash
from flask_app.models.user import User
from flask_app.models.consultation import Consultation
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/new/consultation')
def new_consultation():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_consultation.html',user=User.get_by_id(data))


@app.route('/create/consultation',methods=['POST'])
def create_consultation():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Consultation.validate_consultation(request.form):
        return redirect('/new/consultation')
    data = {
        "stylist_name": request.form["stylist_name"],
        "date": request.form["date"],
        "event": request.form["event"],
        "user_id": session["user_id"]
    }
    Consultation.save(data)
    return redirect('/dashboard')

@app.route('/edit/consultation/<int:id>')
def edit_consultation(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_consultation.html", edit=Consultation.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/consultation/', methods=['POST'])
def update_consultation():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Consultation.validate_consultation(request.form):
        return redirect('/new/consultation')
    data = {
        "stylist_name": request.form["stylist_name"],
        "date": request.form["date"],
        "event": request.form["event"],
        "id": request.form["id"]
    }
    Consultation.update(data)
    return redirect('/dashboard')

@app.route('/consultation/<int:id>')
def show_consultation(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_consultation.html",consultation=Consultation.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/consultation/<int:id>')
def destroy_consultation(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Consultation.destroy(data)
    return redirect('/dashboard')