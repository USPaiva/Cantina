from Site_cantina import database, login
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(16), nullable=False, unique=True)
    password = database.Column(database.String(60), nullable=False)  # Aumente para armazenar hash de senha segura
    email = database.Column(database.String(255), nullable=False, unique=True)  # Garanta que o e-mail seja único
    ativo = database.Column(database.Boolean, nullable=False, default=True)  # Pode ser padrão para True
    type = database.Column(database.String(45), nullable=False)  # Verifique se esse campo precisa ser nullable ou não

    #orders = database.relationship('Order', backref='user', lazy=True)

class PaymentType(database.Model):
    __tablename__ = 'tipo_pagamento'
    id = database.Column('Id', database.Integer, primary_key=True, autoincrement=True)
    payment_type = database.Column('tipo_pagamento', database.String(45), nullable=False, unique=True)

    orders = database.relationship('Order', backref='payment_type', lazy=True)

class Order(database.Model):
    __tablename__ = 'pedidos'
    id = database.Column('Id', database.Integer, primary_key=True)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    retirada = database.Column(database.DateTime, nullable=False)
    valor = database.Column(database.String(45), nullable=False)
    user_id = database.Column('user_Id', database.Integer, database.ForeignKey('user.id'), nullable=False)
    payment_type_id = database.Column('tipo_pagamento_Id', database.Integer, database.ForeignKey('tipo_pagamento.Id'), nullable=False)

    products = database.relationship('ProductOrder', backref='order', lazy=True)

class Product(database.Model):
    __tablename__ = 'produto'
    id = database.Column('Id', database.Integer, primary_key=True, autoincrement=True)
    quantidade = database.Column(database.Integer, nullable=False)
    nome = database.Column(database.String(40), nullable=False, unique=True)
    valor_compra = database.Column('valorCompra', database.Float, nullable=False)
    valor_venda = database.Column('valorVenda', database.Float, nullable=False)
    descricao = database.Column(database.String(45), nullable=False)
    foto = database.Column(database.String(120), nullable=False, unique=True)

    product_orders = database.relationship('ProductOrder', backref='product', lazy=True)

class ProductOrder(database.Model):
    __tablename__ = 'produto_has_pedidos'
    product_id = database.Column('produto_Id', database.Integer, database.ForeignKey('produto.Id'), primary_key=True)
    order_id = database.Column('pedidos_Id', database.Integer, database.ForeignKey('pedidos.Id'), primary_key=True)
    quantidade = database.Column(database.Integer, nullable=False)