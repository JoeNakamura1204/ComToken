from functools import wraps

from flask import render_template, request, redirect, url_for, flash, abort, jsonify, session, g

from comtoken import db, app
from comtoken.form import LoginForm
from comtoken.model import Entry, User


def login_required(f):
    @wraps(f)
    def decorated_view(*args,**kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.path))
        return f(*args,**kwargs)
    return decorated_view

@app.before_request
def load_user():
    user_id=session.get('user_id')
    if user_id is None:
       g.user = None
    else:
        g.user = User.query.get(session['user_id'])

@app.route('/')
def top():
    entries = Entry.query.all()
    return render_template('top.html')

@app.route('/entries')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html',entries=entries)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user,authenticated = User.authenticate(db.session.query,form.email.data,form.password.data)
        if authenticated:
            session['user_id']=user.id
            flash('You were logged in')
            return redirect(url_for('user_detail',user_id=user.id))
        else:
            flash('MailアドレスかPasswordが違います')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/add',methods=['POST'])
def add_entry():
    entry = Entry(
        title = request.form['title'],
        text = request.form['text']
    )
    db.session.add(entry)
    db.session.commit()
    flash("New Entry was successfully posted")
    return redirect(url_for('show_entries'))

@app.route('/users/')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users = users)

@app.route('/users/<int:user_id>/')
@login_required
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user/detail.html',user=user)

@app.route('/users/<int:user_id>/edit/' ,methods=['GET','POST'])
@login_required
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method=='POST':
        name = request.form['name'],
        email = request.form['email'],
        password = request.form['password'],
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_detail',user_id=user_id))
    return render_template('user/edit.html', user=user)

@app.route('/user/create/' ,methods=['GET','POST'])
@login_required
def user_create():
    if request.method =='POST':
        user = User(
            name = request.form['name'],
            email = request.form['email'],
            password = request.form['password'],
            belonging = request.form['belonging'],
            hobby = request.form['hobby'],
            gender = request.form['gender'],
            house = request.form['house'],
            description = request.form['description']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('user/edit.html')

@app.route('/signup')
def signup():
    return render_template('user/create.html')


@app.route('/createnew/' ,methods=['GET','POST'])
def create_newuser():
    if request.method =='POST':
        user = User(
            name = request.form['name'],
            email = request.form['email'],
            password = request.form['password'],
            belonging = request.form['belonging'],
            hobby = request.form['hobby'],
            gender = request.form['gender'],
            house = request.form['house'],
            description = request.form['description']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('top.html')

@app.route('/user/<int:user_id>/delete/' ,methods=['DELETE'])
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response =jsonify({'status':'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status':'OK'})