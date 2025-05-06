from flask import render_template, redirect, url_for
from . import main
from .. import db


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reset-db')
def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return redirect(url_for('main.index'))
