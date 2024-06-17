from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class FormLogin(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=32)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('senha')])
    type = StringField("Tipo de Usuário", validators=[DataRequired(), Length(max=45)])
    botao_confirmacao = SubmitField("Criar Conta")

class FormCriarContaCliente(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=32)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('senha')])
    type = "Cliente"
    botao_confirmacao = SubmitField("Criar Conta")
    

class FormUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=32)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    ativo = BooleanField("Ativo", validators=[DataRequired()])
    type = StringField("Tipo de Usuário", validators=[DataRequired(), Length(max=45)])
    botao_confirmacao = SubmitField("Salvar")

class FormPaymentType(FlaskForm):
    payment_type = StringField("Tipo de Pagamento", validators=[DataRequired(), Length(max=45)])
    botao_confirmacao = SubmitField("Salvar")

class FormOrder(FlaskForm):
    date = DateTimeField("Data", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    retirada = DateTimeField("Data de Retirada", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    valor = StringField("Valor", validators=[DataRequired(), Length(max=45)])
    quantidade = IntegerField("Quantidade", validators=[DataRequired()])
    user_id = IntegerField("ID do Usuário", validators=[DataRequired()])
    payment_type_id = IntegerField("ID do Tipo de Pagamento", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Salvar")

class FormProduct(FlaskForm):
    quantidade = IntegerField("Quantidade", validators=[DataRequired()])
    nome = StringField("Nome", validators=[DataRequired(), Length(max=40)])
    valor_compra = FloatField("Valor de Compra", validators=[DataRequired()])
    valor_venda = FloatField("Valor de Venda", validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[DataRequired(), Length(max=45)])
    foto = FileField("Foto", validators=[DataRequired()])  # Adiciona o campo para upload de arquivos
    botao_confirmacao = SubmitField("Salvar")

class FormProductOrder(FlaskForm):
    product_id = IntegerField("ID do Produto", validators=[DataRequired()])
    order_id = IntegerField("ID do Pedido", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Salvar")