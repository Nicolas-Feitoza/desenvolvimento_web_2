from flask import render_template, redirect, url_for, flash
from .. import db
from ..models import User, Role
from . import main
from .forms import CadastrarProfessor
from datetime import datetime
from functools import wraps


# Rota Principal
@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

def rota_indisponivel(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return render_template('nao_disponivel.html', current_time=datetime.utcnow())
    return decorated_function

@main.route('/disciplinas')
@rota_indisponivel
def disciplinas():
    pass

@main.route('/alunos')
@rota_indisponivel
def alunos():
    pass

@main.route('/cursos')
@rota_indisponivel
def cursos():
    pass

@main.route('/ocorrencias')
@rota_indisponivel
def ocorrencias():
    pass

@main.route('/professores', methods=['GET', 'POST'])
def cadastrar_professores():
    """
    Rota para cadastro e exibição de professores associados a disciplinas.
    """
    form = CadastrarProfessor()

    # Processar o formulário no caso de um POST
    if form.validate_on_submit():
        # Verificar se o professor já está registrado
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            role = Role.query.filter_by(name=form.role.data).first()
            if role:
                # Criar e salvar o novo professor
                user = User(username=form.name.data, role=role)
                db.session.add(user)
                db.session.commit()
                flash(f"Professor {form.name.data} cadastrado com sucesso na disciplina {role.name}!")
            else:
                flash("Disciplina selecionada não encontrada no banco de dados.", "error")
        else:
            flash(f"O professor {form.name.data} já está registrado.", "warning")
        return redirect(url_for('main.cadastrar_professores'))
    # Obter todos os professores para exibição na tabela
    users = User.query.all()
    return render_template(
        'cadastro_de_professores.html',
        form=form,
        users=users
    )

# Rota para Reinicializar o Banco de Dados
@main.route('/reset-db')
def reset_db():
    db.drop_all()
    db.create_all()
    dsw=Role(name='DSWA5')
    gps=Role(name='GPSA5')
    ihc=Role(name='IHCA5')
    sod=Role(name='SODA5')
    pji=Role(name='PJIA5')
    tco=Role(name='TCOA5')
    db.session.add_all([dsw, gps, ihc, sod, pji, tco])
    db.session.commit()
    return redirect(url_for('main.index'))



