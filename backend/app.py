from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Cupcake, Pedido, ItemPedido
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Rotas para Cupcakes
@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    return jsonify([cupcake.to_dict() for cupcake in cupcakes])

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake.to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    cupcake = Cupcake(
        sabor=data['sabor'],
        preco=data['preco'],
        descricao=data.get('descricao', ''),
        imagem=data.get('imagem', ''),
        estoque=data.get('estoque', 0)
    )
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake.to_dict()), 201

# Rotas para Pedidos
@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    data = request.json
    
    # Criar pedido
    pedido = Pedido(
        cliente_nome=data['cliente_nome'],
        cliente_email=data['cliente_email'],
        cliente_endereco=data['cliente_endereco'],
        total=data['total']
    )
    db.session.add(pedido)
    db.session.flush()  # Para obter o ID do pedido
    
    # Criar itens do pedido
    for item in data['itens']:
        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            cupcake_id=item['cupcake_id'],
            quantidade=item['quantidade'],
            preco_unitario=item['preco_unitario']
        )
        db.session.add(item_pedido)
    
    db.session.commit()
    return jsonify({'id': pedido.id, 'message': 'Pedido criado com sucesso!'}), 201

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    resultado = []
    for pedido in pedidos:
        pedido_dict = {
            'id': pedido.id,
            'cliente_nome': pedido.cliente_nome,
            'cliente_email': pedido.cliente_email,
            'total': pedido.total,
            'status': pedido.status,
            'data_criacao': pedido.data_criacao.isoformat()
        }
        resultado.append(pedido_dict)
    return jsonify(resultado)

# Função para inicializar banco de dados
def init_db():
    with app.app_context():
        db.create_all()
        
        # Adicionar dados de exemplo apenas se a tabela estiver vazia
        if Cupcake.query.count() == 0:
            cupcakes_exemplo = [
                Cupcake(sabor="Chocolate", preco=8.50, descricao="Delicioso cupcake de chocolate belga", imagem="images/chocolate.jpg", estoque=20),
                Cupcake(sabor="Morango", preco=9.00, descricao="Cupcake com recheio de morango fresco", imagem="https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=400&h=300&fit=crop", estoque=15),
                Cupcake(sabor="Baunilha", preco=7.50, descricao="Clássico cupcake de baunilha com frosting", imagem="https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=400&h=300&fit=crop", estoque=25),
                Cupcake(sabor="Red Velvet", preco=10.00, descricao="Cupcake vermelho com cream cheese", imagem="https://images.unsplash.com/photo-1614707267537-b85aaf00c4b7?w=400&h=300&fit=crop", estoque=12)
            ]
            db.session.bulk_save_objects(cupcakes_exemplo)
            db.session.commit()
            print("✅ Banco de dados inicializado com dados de exemplo!")

# Inicializar o banco de dados antes do primeiro request
@app.before_request
def before_first_request():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

if __name__ == '__main__':
    # Garantir que o banco seja criado ao iniciar o app
    init_db()
    app.run(debug=True, port=5000)