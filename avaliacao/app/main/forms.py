from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Regexp, Length
from app.models import User

# Validação customizada para verificar nome único
def UniqueName(message=None):
    def _validate_name(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message or 'Este nome já está registrado.')
    return _validate_name

class CadastrarProfessor(FlaskForm):
    name = StringField('Cadastre o professor:',
                        validators=[
                            DataRequired(message="O campo de nome é obrigatório."),
                            Length(1, 64),
                            Regexp(
                                '^[a-zA-Z][a-zA-Z0-9_. ]*$', 0,
                                message='O nome de usuário deve ter apenas letras, números, pontos ou sublinhados'
                            ),
                            UniqueName(message="Este professor já está registrado.")
                        ],
                        render_kw={"placeholder": "Digite o nome completo do professor"}
    )
    role = SelectField('Disciplina associada:',
                       choices=[
                           ('DSWA5', 'DSWA5'), ('GPSA5', 'GPSA5'), ('IHCA5', 'IHCA5'),
                           ('SODA5', 'SODA5'), ('PJIA5', 'PJIA5'), ('TCOA5', 'TCOA5')
                       ],
                       validators=[DataRequired(message="É obrigatório selecionar uma disciplina.")]
    )
    submit = SubmitField('Cadastrar')