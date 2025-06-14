from flask import Blueprint, request, jsonify
from src.models.estoque import db, Produto, Movimentacao

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Listar todos os produtos"""
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Obter detalhes de um produto específico"""
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())

@produto_bp.route('/produtos', methods=['POST'])
def adicionar_produto():
    """Adicionar um novo produto"""
    data = request.get_json()
    
    if not data or 'nome' not in data:
        return jsonify({'erro': 'Nome do produto é obrigatório'}), 400
    
    produto = Produto(
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        quantidade=data.get('quantidade', 0)
    )
    
    try:
        db.session.add(produto)
        db.session.commit()
        return jsonify(produto.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao adicionar produto'}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualizar um produto existente"""
    produto = Produto.query.get_or_404(produto_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    
    produto.nome = data.get('nome', produto.nome)
    produto.descricao = data.get('descricao', produto.descricao)
    produto.quantidade = data.get('quantidade', produto.quantidade)
    
    try:
        db.session.commit()
        return jsonify(produto.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao atualizar produto'}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def excluir_produto(produto_id):
    """Excluir um produto"""
    produto = Produto.query.get_or_404(produto_id)
    
    try:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Produto excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao excluir produto'}), 500

