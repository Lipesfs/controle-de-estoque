from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    
    # Relacionamento com movimentações
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade
        }

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'producao', 'venda', 'transferencia_loja_galpao', 'transferencia_galpao_loja'
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    origem_destino = db.Column(db.String(50))  # 'loja', 'galpao', 'producao', 'venda'

    def __repr__(self):
        return f'<Movimentacao {self.tipo} - {self.quantidade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'tipo': self.tipo,
            'quantidade': self.quantidade,
            'data': self.data.isoformat() if self.data else None,
            'origem_destino': self.origem_destino
        }

