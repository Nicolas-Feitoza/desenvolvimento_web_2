from flask import render_template, session, redirect, url_for, flash, current_app
from .. import db
from ..models import User
from ..email import send_simple_message
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que lida com a submissão de formulário e exibe usuários cadastrados.
    """
    form = NameForm()

    # Lógica para tratar a submissão do formulário
    if form.validate_on_submit():
        # Verifica se o usuário já existe no banco de dados
        user = User.query.filter_by(prontuario=form.prontuario.data).first()

        if user is None:
            # Se o usuário não existe, cria um novo e salva no banco de dados
            user = User(username=form.name.data, prontuario=form.prontuario.data)
            db.session.add(user)
            db.session.commit()

            # Define que este é um novo usuário
            session['known'] = False
            flash('Você está cadastrado! O administrador será notificado.')

            # Configura a lista de destinatários para o e-mail de notificação
            recipients = [current_app.config['FLASKY_ADMIN']]
            if form.notificar_admin.data:
                recipients.append('flaskaulasweb@zohomail.com')

            # Envia e-mail notificando sobre o novo cadastro
            send_simple_message(
                to=recipients,
                subject='Novo usuário cadastrado',
                new_user=f"Nome: {form.name.data}, Prontuário: {form.prontuario.data}, ID: {user.id}"
            )
        else:
            # Se o usuário já existe, informa ao usuário
            session['known'] = True
            flash('Prontuário já cadastrado!')

        # Armazena o nome na sessão para uso posterior
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    # Obtém todos os usuários cadastrados para exibição
    users = User.query.all()
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        users=users
    )
