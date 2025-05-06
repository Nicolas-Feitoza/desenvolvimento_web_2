from itsdangerous import URLSafeTimedSerializer,BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from flask import current_app

# Modelo para cargos ou papéis no sistema
class Role(db.Model):
    __tablename__ = 'roles'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(64), unique=True, nullable=False)  # Nome do papel, único e obrigatório
    users = db.relationship('User', backref='role', lazy='dynamic')  # Relacionamento com a tabela User

    def __repr__(self):
        """
        Representação amigável do objeto Role.
        Retorna uma string com o nome do papel.
        """
        return f'<Role {self.name}>'

    def save(self):
        """
        Salva ou atualiza o registro no banco de dados.
        Possíveis erros:
        - IntegrityError: Se houver tentativa de salvar um papel com o mesmo nome já existente (violação de unicidade).
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao salvar o papel '{self.name}': {str(e)}")

    def delete(self):
        """
        Remove o registro do banco de dados.
        Possíveis erros:
        - IntegrityError: Se o papel estiver associado a algum usuário (violação de integridade referencial).
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao deletar o papel '{self.name}': {str(e)}")

# Modelo para usuários
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)  # Nome do usuário, único e indexado
    prontuario = db.Column(db.String(10), unique=True, nullable=False)  # Prontuário único e obrigatório
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único e obrigatório
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Chave estrangeira referenciando Role
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    # Criação de uma propriedade somente para leitura chamada password
    # Tentativa de ler a propriedade password resultará em um erro
    @property
    def password(self):
        raise AttributeError('Password não é um atributo legível.')

    # Quando a propriedade password for definida, o método setter chamará a função generate_password_hash
    # e escreverá o resultado no campo password_hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Compara senha fornecida pelo usuário com o hash armazenado
    # Se True, senha correta
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        secret_key = current_app.config['SECRET_KEY']
        # Garantir que a chave secreta esteja no formato correto
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        # Criando o Serializer
        s = URLSafeTimedSerializer(secret_key)
        # Gerando o token com expiração
        token = s.dumps({'confirm': self.id}, salt='confirmation')
        return token

    def confirm(self, token):
        try:
            # Obter a chave secreta do aplicativo
            secret_key = current_app.config['SECRET_KEY']
            if isinstance(secret_key, str):
                secret_key = secret_key.encode('utf-8')
            # Criando o Serializer
            s = URLSafeTimedSerializer(secret_key)
            # Decodificação do token com salt e expiration no método loads
            data = s.loads(token, salt='confirmation')  # max_age define a expiração do token
            # Comparação do IDs
            if data.get('confirm') == self.id:
                # Marcar o usuário como confirmado
                self.confirmed = True
                self.save()  # Salvar o usuário com a atualização do campo 'confirmed'
                return True
            return False
        except (SignatureExpired, BadSignature):
            return False  # Retorna False se o token expirou


    def __repr__(self):
        """
        Representação amigável do objeto User.
        Retorna uma string com o nome e prontuário do usuário.
        """
        return f'<User {self.username} - Prontuário {self.prontuario}>'

    def save(self):
        """
        Salva ou atualiza o registro no banco de dados.
        Possíveis erros:
        - IntegrityError: Se houver duplicidade nos campos 'username', 'prontuario' ou 'email'.
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao salvar o usuário '{self.username}': {str(e)}")

    def delete(self):
        """
        Remove o registro do banco de dados.
        Possíveis erros:
        - SQLAlchemyError: Qualquer erro de banco de dados durante a exclusão.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao deletar o usuário '{self.username}': {str(e)}")

    @staticmethod
    def get_user_by_email(email):
        """
        Busca um usuário no banco de dados pelo email.

        :param email: Email do usuário a ser buscado.
        :return: Instância do usuário ou None se não encontrado.
        Possíveis erros:
        - SQLAlchemyError: Qualquer erro ao realizar a consulta no banco de dados.
        """
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário com email '{email}': {str(e)}")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
