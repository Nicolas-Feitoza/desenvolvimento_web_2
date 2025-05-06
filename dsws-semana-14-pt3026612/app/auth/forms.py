from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

# Validação customizada para verificar domínio de e-mail def ZohoEmail(message=None):
def ZohoEmail(message=None):
    def _validate_email(form, field):
        if not field.data.endswith('@zohomail.com'):
            raise ValidationError(message or 'Por favor, use um e-mail @zohomail.com.')
    return _validate_email

# Validação customizada para verificar e-mail único
def UniqueEmail(message=None):
    def _validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message or 'Este e-mail já está registrado.')
    return _validate_email

# Validação customizada para verificar prontuário único
def UniqueProntuario(message=None):
    def _validate_prontuario(form, field):
        if User.query.filter_by(prontuario=field.data).first():
            raise ValidationError(message or 'Este prontuário já está registrado.')
    return _validate_prontuario

def UniqueUsername(message=None):
    def _validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message or 'Este nome já está em uso.')
    return _validate_username

class LoginForm(FlaskForm):
    email = StringField('Digite seu email', validators=[
        DataRequired(message="O campo de email é obrigatório."),
        Length(1, 64),
        Email(message="Insira um e-mail válido."),
        ZohoEmail(message='Por favor, use um e-mail "@zohomail.com".')
        ], render_kw={"placeholder": "Digite seu email"})

    password = PasswordField('Digite sua senha', validators=[
        DataRequired(message="O campo de senha é obrigatório.")
        ], render_kw={"placeholder": "Digite sua senha"})

    remember_me = BooleanField('Mantenha-me conectado')
    submit = SubmitField("Entrar")

class RegistrationForm(FlaskForm):
    email = StringField(
        'Digite seu email',
        validators=[DataRequired(message="O campo de email é obrigatório."),
        Length(1, 64),
        Email(message="Insira um e-mail válido."),
        UniqueEmail(message="Este e-mail já está registrado."),
        ZohoEmail(message="Por favor, use um e-mail @zohomail.com.")
        ], render_kw={"placeholder": "Digite seu email"})

        # Campo para o nome do usuário
    username = StringField(
            'Qual é o seu nome?',
            validators=[DataRequired(message="O campo de nome é obrigatório."),
            Length(1, 64),
            Regexp(
                '^[a-zA-Z][a-zA-Z0-9_. ]*$', 0,
                message='O nome de usuário deve ter apenas letras, números, pontos ou sublinhados'
            ),
            UniqueUsername(message="Este nome já está em uso.")],
            render_kw={"placeholder": "Digite seu nome completo"}
    )
        # Campo para o prontuário com validação de formato
    prontuario = StringField(
        'Digite seu prontuário',
        validators=[
            DataRequired(message="O campo de prontuário é obrigatório."),
            Regexp(
                r'^[a-zA-Z]{3}\d{7}$',
                message='O prontuário deve ter 3 letras seguidas de 7 números. Exemplo: ABC1234567'
            ),
            UniqueProntuario(message="Este prontuário já está registrado.")  # Validação para prontuário único
        ],
        render_kw={"placeholder": "Exemplo: ABC1234567"}
    )


    password = PasswordField(
            'Digite sua senha',
            validators=[DataRequired(message="O campo de senha é obrigatório."),
            EqualTo('password2', message='Senhas devem coincidir.')
            ], render_kw={"placeholder": "Digite sua senha"}
    )
    password2 = PasswordField(
            'Confirmar senha',
            validators=[DataRequired(message="As senhas devem ser iguais.")],
            render_kw={"placeholder": "Confirmar senha"}
    )
    submit = SubmitField("Registrar")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Senha antiga', validators=[DataRequired()])
    password = PasswordField('Nova senha', validators=[
        DataRequired(), EqualTo('password2', message='Senhas devem coincidir.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Atualizar senha')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="O campo de email é obrigatório."), Length(1, 64),
                                             Email(message="Insira um e-mail válido.")
                                             ], render_kw={"placeholder": "Digite seu email"})
    submit = SubmitField('Nova senha')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[
        DataRequired(message="O campo de senha é obrigatório."),
        EqualTo('password2', message='Senhas devem coincidir')],
        render_kw={"placeholder": "Digite sua nova senha"})
    password2 = PasswordField('Confirmar senha', validators=[DataRequired()],
        render_kw={"placeholder": "Confirmar senha"})
    submit = SubmitField('Redefinir senha')

class ChangeEmailForm(FlaskForm):
    email = StringField('Novo email', validators=[DataRequired(message="O campo de email é obrigatório."),
                                                  Length(1, 64),
                                                  Email(message="Insira um e-mail válido."),
                                                  UniqueEmail(message="Este e-mail já está registrado."),
                                                  ZohoEmail(message="Por favor, use um e-mail @zohomail.com.")
                                                  ], render_kw={"placeholder": "Digite seu novo email"})
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
