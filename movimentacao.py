from flask import Blueprint, request, jsonify
from src.models.estoque import db, Produto, Movimentacao

movimentacao_bp = Blueprint('movimentacao', __name__)

@movimentacao_bp.route('/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    """Listar todas as movimentações"""
    movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).all()
    return jsonify([mov.to_dict() for mov in movimentacoes])

@movimentacao_bp.route('/movimentacoes', methods=['POST'])
def registrar_movimentacao():
    """Registrar uma nova movimentação"""
    data = request.get_json()
    
    if not data or 'produto_id' not in data or 'tipo' not in data or 'quantidade' not in data:
        return jsonify({'erro': 'Dados obrigatórios: produto_id, tipo, quantidade'}), 400
    
    produto = Produto.query.get_or_404(data['produto_id'])
    tipo = data['tipo']
    quantidade = int(data['quantidade'])
    
    # Validar tipos de movimentação
    tipos_validos = ['producao', 'venda', 'transferencia_loja_galpao', 'transferencia_galpao_loja']
    if tipo not in tipos_validos:
        return jsonify({'erro': f'Tipo inválido. Tipos válidos: {tipos_validos}'}), 400
    
    # Calcular nova quantidade do produto
    if tipo in ['producao', 'transferencia_galpao_loja']:
        # Entrada de estoque
        nova_quantidade = produto.quantidade + quantidade
        origem_destino = 'galpao' if tipo == 'producao' else 'loja'
    elif tipo in ['venda', 'transferencia_loja_galpao']:
        # Saída de estoque
        if produto.quantidade < quantidade:
            return jsonify({'erro': 'Quantidade insuficiente em estoque'}), 400
        nova_quantidade = produto.quantidade - quantidade
        origem_destino = 'venda' if tipo == 'venda' else 'galpao'
    
    # Criar movimentação
    movimentacao = Movimentacao(
        produto_id=data['produto_id'],
        tipo=tipo,
        quantidade=quantidade,
        origem_destino=origem_destino
    )
    
    try:
        # Atualizar quantidade do produto
        produto.quantidade = nova_quantidade
        
        # Salvar movimentação
        db.session.add(movimentacao)
        db.session.commit()
        
        return jsonify(movimentacao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao registrar movimentação'}), 500

