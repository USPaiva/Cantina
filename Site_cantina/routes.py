import os
from flask import flash, json, render_template, request, url_for, redirect, session
import logging
from Site_cantina import ALLOWEDEXTENSIONS, app, database, bcrypt
from datetime import datetime
from flask_login import  login_user, current_user, logout_user, login_required
from Site_cantina.models import User, Product, PaymentType, Order, ProductOrder
from Site_cantina.forms import FormLogin, FormCriarConta, FormCriarContaCliente, FormUser, FormPaymentType, FormOrder, FormProduct, FormProductOrder
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWEDEXTENSIONS

# Rota para renderizar a página de cadastro de produto
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    form = FormProduct()

    if form.validate_on_submit():
        nome = form.nome.data
        descricao = form.descricao.data
        valor_compra = form.valor_compra.data
        valor_venda = form.valor_venda.data
        quantidade = form.quantidade.data
        foto = form.foto.data

        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            relative_path = os.path.join('produtos', filename).replace("\\",'/')
            novo_produto = Product(
                nome=nome,
                descricao=descricao,
                valor_compra=valor_compra,
                valor_venda=valor_venda,
                quantidade=quantidade,
                foto=relative_path  # Salvar apenas o caminho relativo
            )

            try:
                database.session.add(novo_produto)
                database.session.commit()
                flash('Produto cadastrado com sucesso!', 'success')
                return redirect(url_for('cadastrar_produto'))
            except Exception as e:
                database.session.rollback()
                flash(f'Ocorreu um erro ao cadastrar o produto: {e}', 'danger')
        else:
            flash('Tipo de arquivo não permitido.', 'danger')

    return render_template('cadastrar_produto.html', user=current_user, form=form)

# Rota para renderizar a página de verificação de estoque
@app.route('/verificar_estoque', methods=["GET"])
def verificar_estoque():
    produtos = Product.query.all()
    return render_template('verificar_estoque.html', produtos=produtos)

# Rota para renderizar a pÃ¡gina de editar produto
@app.route('/editar_produto/<int:id>', methods=["GET", "POST"])
def editar_produto(id):
    produto = Product.query.get_or_404(id)
    form = FormProduct(obj=produto)
    
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.quantidade = form.quantidade.data
        produto.valor_compra = form.valor_compra.data
        produto.valor_venda = form.valor_venda.data
        produto.descricao = form.descricao.data
        
        # Verifica se uma nova foto foi enviada
        if form.foto.data:
            # Salva a nova foto
            foto = form.foto.data
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            produto.foto = filename
        
        try:
            database.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('verificar_estoque'))
        except Exception as e:
            database.session.rollback()
            flash(f'Erro ao atualizar o produto: {e}', 'danger')
    
    return render_template('editar_produto.html', form=form, produto=produto)

# Rota para renderizar a página de login
@app.route('/', methods=["GET", "POST"])
def index():
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Adicione logs para depuração
            print(f"Usuário encontrado: {user.username}")
            print(f"Senha armazenada (hash): {user.password}")
            print(f"Senha inserida: {form.senha.data}")

            if user.password == form.senha.data:  # bcrypt.check_password_hash(user.password, form.senha.data)
                print("Senha correta")
                login_user(user, remember=True)
                flash('Login feito com sucesso!', 'success')
                next_page = request.args.get('next')
                if user.type == 'Admin':
                    return redirect(next_page) if next_page else redirect(url_for("admin_dashboard"))
                elif user.type == 'Funcionario':
                    return redirect(next_page) if next_page else redirect(url_for("funcionario_dashboard"))
                else:
                    return redirect(next_page) if next_page else redirect(url_for("pedir", user=user.username))
            else:
                print("Senha incorreta")
                flash('Login ou senha incorretos. Tente novamente.', 'danger')
        else:
            print("Usuário não encontrado")
            flash('Usuário não encontrado.', 'danger')
    return render_template('login.html', user=current_user, form=form)

@app.route('/pedir/<user>', methods=["GET", "POST"])
@login_required
def pedir(user):
    # Aqui você precisa obter o objeto User correto
    user_obj = User.query.filter_by(username=user).first()

    # Verifique se o usuário existe no banco de dados antes de tentar fazer login
    if user_obj:
        login_user(user_obj, remember=True)
        produtos = Product.query.all()
        return render_template('vitrine.html', user=current_user, form=FormOrder(), produtos=produtos)
    else:
        # Caso o usuário não exista, faça alguma manipulação de erro ou redirecione
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('login'))  # Redirecionar para a página de login ou outra página apropriada

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/finalizar_pedido', methods=["GET", "POST"])
@login_required
def finalizar_pedido():
    if request.method == "POST":
        # Obter o carrinho do formulário
        cart_json = request.form.get('cart')
        logging.debug(f'Carrinho JSON: {cart_json}')
        
        if not cart_json:
            flash('Carrinho vazio!', 'danger')
            return redirect(url_for('pedir', user=current_user.username))
        
        # Converter o carrinho de JSON para um objeto Python
        try:
            cart = json.loads(cart_json)
        except json.JSONDecodeError as e:
            logging.error(f'Erro ao decodificar o JSON do carrinho: {e}')
            flash('Ocorreu um erro ao processar o carrinho. Por favor, tente novamente.', 'danger')
            return redirect(url_for('finalizar_pedido'))
        
        logging.debug(f'Carrinho: {cart}')
        
        # Obter dados do formulário
        pickup_date = request.form.get('pickup-date')
        pickup_time = request.form.get('pickup-time')
        payment_method = request.form.get('payment-method')
        
        logging.debug(f'Pickup Date: {pickup_date}')
        logging.debug(f'Pickup Time: {pickup_time}')
        logging.debug(f'Payment Method: {payment_method}')
        
        # Validar dados do formulário
        if not pickup_date or not pickup_time or not payment_method:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('finalizar_pedido'))
        
        try:
            # Criar novo pedido
            retirada_datetime = datetime.strptime(f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M")
            valor_total = sum(float(item['price']) * item['quantity'] for item in cart)
            logging.debug(f'Retirada Datetime: {retirada_datetime}')
            logging.debug(f'Valor Total: {valor_total}')
            
            novo_pedido = Order(
                date=datetime.utcnow(),
                retirada=retirada_datetime,
                valor=str(valor_total),  # Salvar como string conforme o modelo
                user_id=current_user.id,
                payment_type_id=int(payment_method)  # Usar o ID do tipo de pagamento diretamente
            )
            database.session.add(novo_pedido)
            database.session.commit()  # Commit do pedido para obter o novo pedido ID
            
            # Adicionar produtos ao pedido e atualizar a quantidade no estoque
            for item in cart:
                produto = Product.query.get(int(item['id']))
                if produto.quantidade < int(item['quantity']):
                    flash(f"Estoque insuficiente para o produto {produto.nome}.", 'danger')
                    database.session.rollback()
                    return redirect(url_for('finalizar_pedido'))
                
                produto.quantidade -= int(item['quantity'])
                novo_produto_pedido = ProductOrder(
                    product_id=produto.id,
                    order_id=novo_pedido.id,
                    quantidade=int(item['quantity'])  # Certifique-se de que 'quantity' existe no item
                )
                database.session.add(novo_produto_pedido)
                database.session.add(produto)  # Atualiza o produto no banco de dados
            
            database.session.commit()  # Commit das associações e atualizações de estoque
            
            # Limpar carrinho
            session.pop('cart', None)
            
            flash('Pedido confirmado com sucesso!', 'success')
            return redirect(url_for('visualizar_pedido'))
        
        except Exception as e:
            logging.error(f'Erro ao finalizar pedido: {e}')
            flash('Ocorreu um erro ao processar seu pedido. Por favor, tente novamente.', 'danger')
            return redirect(url_for('finalizar_pedido'))
    
    # Obter todos os tipos de pagamento existentes
    payment_types = PaymentType.query.all()
    cart = session.get('cart', {})
    total = sum(details['subtotal'] for details in cart.values())
    return render_template('finalizar_pedido.html', user=current_user.username, cart=cart, total=total, payment_types=payment_types)
@app.route('/criar_tipo_pagamento', methods=["GET", "POST"])
@login_required
def criar_tipo_pagamento():
    if request.method == 'POST':
        payment_type = request.form.get('payment-type')
        
        if not payment_type:
            flash('O campo Tipo de Pagamento é obrigatório!', 'danger')
            return redirect(url_for('criar_tipo_pagamento'))
        
        # Verificar se o tipo de pagamento já existe
        existing_payment_type = PaymentType.query.filter_by(payment_type=payment_type).first()
        if existing_payment_type:
            flash('Este tipo de pagamento já existe!', 'danger')
            return redirect(url_for('criar_tipo_pagamento'))
        
        # Criar novo tipo de pagamento
        novo_tipo_pagamento = PaymentType(payment_type=payment_type)
        database.session.add(novo_tipo_pagamento)
        database.session.commit()
        
        flash('Novo tipo de pagamento criado com sucesso!', 'success')
        return redirect(url_for('criar_tipo_pagamento'))
    
    # Obter todos os tipos de pagamento existentes para exibição na tabela
    payment_types = PaymentType.query.all()
    return render_template('criar_tipo_pagamento.html', user=current_user, payment_types=payment_types)

@app.route('/remover_tipo_pagamento/<int:payment_type_id>', methods=["POST"])
@login_required
def remover_tipo_pagamento(payment_type_id):
    payment_type = PaymentType.query.get_or_404(payment_type_id)
    if payment_type.orders:
        flash('Não é possível remover um tipo de pagamento associado a pedidos!', 'danger')
    else:
        database.session.delete(payment_type)
        database.session.commit()
        flash('Tipo de pagamento removido com sucesso!', 'success')
    return redirect(url_for('criar_tipo_pagamento'))

@app.route('/visualizar_pedido', methods=["GET"])
@login_required
def visualizar_pedido():
    # Verificar se o usuário é administrador
    if current_user.type == 'Admin':
        # Buscar todos os pedidos se o usuário for administrador
        pedidos = Order.query.all()
    else:
        # Buscar pedidos do usuário atual
        pedidos = Order.query.filter_by(user_id=current_user.id).all()

    pedidos_detalhes = []
    for pedido in pedidos:
        produtos_pedido = ProductOrder.query.filter_by(order_id=pedido.id).all()
        produtos = []
        for produto_pedido in produtos_pedido:
            produto = Product.query.get(produto_pedido.product_id)
            produtos.append({
                'nome': produto.nome,
                'quantidade': produto_pedido.quantidade,
                'valor_venda': produto.valor_venda,
                'subtotal': produto_pedido.quantidade * produto.valor_venda
            })
        pedidos_detalhes.append({
            'pedido_id': pedido.id,
            'data': pedido.date.strftime("%d/%m/%Y %H:%M"),
            'retirada': pedido.retirada.strftime("%d/%m/%Y %H:%M"),
            'valor': pedido.valor,
            'produtos': produtos
        })

    return render_template('visualizar_pedido.html',user=current_user, pedidos=pedidos_detalhes)

# Rota para renderizar a página de cadastro de produto
@app.route('/cadastrar_funcionario', methods=["GET", "POST"])
def cadastrar_funcionario():
    
    form = FormCriarConta()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.senha.data, type=form.type.data)
        database.session.add(user)
        database.session.commit()
        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')
        login_user(user, remember=True)
        return redirect(url_for("pedir", user=user.username))
    return render_template('cadastrar_funcionario.html', user=current_user, form=FormCriarConta())

@app.route('/cadastrar_cliente', methods=["GET", "POST"])
def cadastrar_cliente():

    form = FormCriarContaCliente()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.senha.data, type=form.type)
        database.session.add(user)
        database.session.commit()
        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')
        login_user(user, remember=True)
        return redirect(url_for("pedir", user=user.username))
    return render_template('cadastrar_cliente.html', user=current_user, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=["GET", "POST"])
def login():
    redirect(url_for('index'))
    
@app.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.type != 'Admin':
        flash('Acesso negado. Somente administradores podem acessar esta página.', 'danger')
        return redirect(url_for('index'))

    return render_template('admin_dashboard.html', user=current_user)

@app.route('/funcionario', methods=['GET'])
@login_required
def funcionario_dashboard():
    if current_user.type != 'Funcionario':
        flash('Acesso negado. Somente funcionarios podem acessar esta página.', 'danger')
        return redirect(url_for('index'))

    return render_template('funcionario_dashboard.html', user=current_user)

@app.route('/dashboard_redirect')
@login_required
def dashboard_redirect():
    if current_user.type == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.type == 'Funcionario':
        return redirect(url_for('funcionario_dashboard'))
    else:
        return redirect(url_for('pedir', user=current_user.username))