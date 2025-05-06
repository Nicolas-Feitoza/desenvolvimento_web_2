from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError
from app.models import User

# Formulário Flask-WTF para captura de informações do usuário
class NameForm(FlaskForm):
    # Campo para o nome do usuário
    name = StringField(
        'Qual é o seu nome?', 
        validators=[DataRequired()],
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
            )
        ],
        render_kw={"placeholder": "Exemplo: ABC1234567"}
    )
    
    # Campo booleano para notificação por e-mail
    notificar_admin = BooleanField(
        'Deseja enviar e-mail para flaskaulasweb@zohomail.com?'
    )
    
    # Botão de envio do formulário
    submit = SubmitField('Enviar')

    # Validação adicional para prontuário
    def validate_prontuario(self, field):
        """Valida se o prontuário já está cadastrado no banco de dados."""
        if User.query.filter_by(prontuario=field.data).first():
            raise ValidationError('Este prontuário já está cadastrado. Por favor, insira outro.')
