from . import db

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

# Modelo para usuários
class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)  # Nome do usuário, único e indexado
    prontuario = db.Column(db.String(10), unique=True, nullable=False)  # Prontuário único e obrigatório
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Chave estrangeira referenciando Role

    def __repr__(self):
        """
        Representação amigável do objeto User.
        Retorna uma string com o nome e prontuário do usuário.
        """
        return f'<User {self.username} - Prontuário {self.prontuario}>'
