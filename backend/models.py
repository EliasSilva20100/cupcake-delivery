from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cupcake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    imagem = db.Column(db.String(300))
    estoque = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sabor': self.sabor,
            'preco': self.preco,
            'descricao': self.descricao,
            'imagem': self.imagem,
            'estoque': self.estoque
        }

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    cliente_email = db.Column(db.String(100), nullable=False)
    cliente_endereco = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pendente')
    data_criacao = db.Column(db.DateTime, default=db.func.now())
    
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    cupcake_id = db.Column(db.Integer, db.ForeignKey('cupcake.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    
    cupcake = db.relationship('Cupcake')