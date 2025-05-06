from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'Chave forte'

class DataForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    lastname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua instituição:', validators=[DataRequired()])
    discipline = SelectField('Informe sua disciplina:', choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de Projetos', 'Gestão de Projetos')])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():

    form = DataForm()

    remote_addr = None
    host = None

    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que alterou seu nome!')
        session['name'] = form.name.data
        session['lastname'] = form.lastname.data
        session['institution'] = form.institution.data
        session['discipline'] = form.discipline.data

        remote_addr = request.remote_addr
        host = request.host
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        lastname=session.get('lastname'),
        institution=session.get('institution'),
        discipline=session.get('discipline'),
        remote_addr=remote_addr,
        host=host,
        current_time=datetime.utcnow()
    )

@app.route('/clear_session')
def clear_session():
    session.clear()
    flash('Sessão limpa! Você pode testar o formulário novamente.')
    return redirect(url_for('index'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
