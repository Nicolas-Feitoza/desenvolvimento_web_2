from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from .. import db
from ..email import send_verification_email, send_simple_message, send_email_with_gif

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    prontuario=form.prontuario.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        try:
            send_verification_email(to=user.email, subject='Confirme seu cadastro', body=render_template('auth/email/verify_email.html', username=user.username, token=token))
            flash('Um email de confirmação foi enviado para o seu email.', 'info')
        except Exception as e:
            flash('Não foi possível enviar o email de confirmação. Por favor, tente novamente mais tarde ou contate o email na tela de login', 'danger')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Você confirmou sua conta. Obrigado!', 'info')
        # Envia notificações para o administrador e o e-mail da escola
        email_admin = current_app.config['FLASKY_ADMIN']
        recipient_list = ['flaskaulasweb@zohomail.com', email_admin]
        user_message = "Bem-vindo, {}! Seu cadastro foi confirmado.".format(current_user.username)
        send_simple_message(to=recipient_list[0], subject="Novo Cadastro", new_user=current_user.username)
        send_simple_message(to=recipient_list[1], subject="Notificação de Cadastro", new_user=current_user.username)
        # Envia e-mail com GIF de boas-vindas para o usuário
        url = 'https://nicolassf.pythonanywhere.com/static/images/welcome.gif'
        send_email_with_gif(to=current_user.email, subject="Cadastro confirmado", body=user_message, gif_url=url)
    else:
        flash('O link de confirmação é inválido ou expirou.', 'danger')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_verification_email(to=current_user.email, subject='Confirme seu cadastro',
                            body=render_template('auth/email/verify_email.html', username=current_user.username, token=token))
    flash('Um novo email de confirmação foi enviado para o seu email.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('A sua senha foi atualizada.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Senha inválida.', 'danger')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_verification_email(to=user.email, subject='Redefinir senha',
                                    body=render_template('auth/email/reset_password.html', username=user.username, token=token))
        flash('Um email com instrução para a criação de uma nova senha foi enviado para você.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Sua senha foi atualizada.', 'info')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_verification_email(to=new_email, subject='Confirmar endereço de email',
                                    body=render_template('auth/email/change_email.html', user=current_user, token=token))
            flash('Um email com instruções para cadastrar seu novo email foi enviado para você.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha inválido.', 'danger')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Seu endereço de email foi atualizado.', 'info')
    else:
        flash('Requisição inválida.', 'danger')
    return redirect(url_for('main.index'))