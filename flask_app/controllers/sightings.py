from flask import render_template,redirect,session,request, flash, abort, url_for
from flask_app import app
from flask_app.controllers.users import dashboard
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app.models.skeptic import Skeptic

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/sighting/report')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')

    data ={
        'id': session['user_id']
    }
    return render_template("report-sighting.html",user=User.get_by_id(data))

@app.route('/report', methods=['POST'])
def report_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_report(request.form):
        return redirect('/sighting/report')
    data ={ 
        'location': request.form['location'],
        'description': request.form['description'],
        'date': request.form['date'],
        'sasquatch_num': request.form['sasquatch_num'],
        'user_reported_id': request.form['user_reported_id']
    }
    Sighting.save(data)
    return redirect('/dashboard')

@app.route('/view-sighting/<int:sighting_id>/<int:user_reported_id>')
def view_sighting(sighting_id, user_reported_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'sighting_id': sighting_id,
        'user_reported_id': user_reported_id
    }
    added_by=User.user_who_added(data)
    user=User.get_by_id(data)
    sighting=Sighting.get_by_id(data)
    skeptic=User.get_all_skeptics(data)
    return render_template("view-sighting.html", user=user, sighting=sighting, added_by=added_by, skeptic=skeptic)

@app.route('/edit-sighting/<int:sighting_id>')
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'sighting_id': sighting_id
    }
    user=User.get_by_id(data)
    sighting=Sighting.get_by_id(data)
    return render_template("edit-sighting.html", sighting=sighting, user=user)

@app.route('/sighting-update', methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_report(request.form):
        return redirect('/dashboard')
    data ={ 
        'id': session['user_id'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date': request.form['date'],
        'sasquatch_num': request.form['sasquatch_num'],
        'sighting_id': request.form['sighting_id']
    }
    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/skeptic/<int:sighting_skeptic_id>/<int:user_skeptic_id>/<int:user_reported_id>')
def im_a_skeptic(sighting_skeptic_id, user_skeptic_id, user_reported_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'user_skeptic_id': user_skeptic_id,
        'sighting_skeptic_id': sighting_skeptic_id,
        'user_reported_id': user_reported_id
    }
    Skeptic.skeptic(data)
    return redirect(f'/view-sighting/{sighting_skeptic_id}/{user_reported_id}')

@app.route('/believe/<int:sighting_skeptic_id>/<int:user_skeptic_id>/<int:user_reported_id>')
def im_a_believer(sighting_skeptic_id, user_skeptic_id, user_reported_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'user_skeptic_id': user_skeptic_id,
        'sighting_skeptic_id': sighting_skeptic_id,
        'user_reported_id': user_reported_id
    }
    Skeptic.not_a_skeptic(data)
    return redirect(f'/view-sighting/{sighting_skeptic_id}/{user_reported_id}')

@app.route('/destroy/<int:sighting_id>')
def destroy_show(sighting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'sighting_id': sighting_id
    }
    
    Sighting.destroy(data)
    return redirect('/dashboard')