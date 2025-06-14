from flask import Blueprint, jsonify
from src.models.estoque import db, Produto, Movimentacao
from sqlalchemy import func
from datetime import datetime

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorios/estoque_atual', methods=['GET'])
def estoque_atual():
    """Relatório de estoque atual de todos os produtos"""
    produtos = Produto.query.all()
    relatorio = []
    
    for produto in produtos:
        relatorio.append({
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'quantidade_atual': produto.quantidade,
            'status': 'Em estoque' if produto.quantidade > 0 else 'Sem estoque'
        })
    
    return jsonify({
        'titulo': 'Relatório de Estoque Atual',
        'data_geracao': datetime.now().isoformat(),
        'produtos': relatorio,
        'total_produtos': len(produtos),
        'produtos_sem_estoque': len([p for p in produtos if p.quantidade == 0])
    })

@relatorio_bp.route('/relatorios/historico_movimentacoes', methods=['GET'])
def historico_movimentacoes():
    """Relatório de histórico de movimentações"""
    movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).limit(100).all()
    
    return jsonify({
        'titulo': 'Histórico de Movimentações',
        'movimentacoes': [mov.to_dict() for mov in movimentacoes],
        'total_movimentacoes': len(movimentacoes)
    })

@relatorio_bp.route('/relatorios/produtos_em_producao', methods=['GET'])
def produtos_em_producao():
    """Relatório de produtos em produção (últimas movimentações de produção)"""
    # Buscar últimas movimentações de produção
    movimentacoes_producao = db.session.query(
        Movimentacao.produto_id,
        func.max(Movimentacao.data).label('ultima_producao'),
        func.sum(Movimentacao.quantidade).label('total_produzido')
    ).filter(
        Movimentacao.tipo == 'producao'
    ).group_by(Movimentacao.produto_id).all()
    
    relatorio = []
    for mov in movimentacoes_producao:
        produto = Produto.query.get(mov.produto_id)
        if produto:
            relatorio.append({
                'produto_id': produto.id,
                'produto_nome': produto.nome,
                'ultima_producao': mov.ultima_producao.isoformat() if mov.ultima_producao else None,
                'total_produzido': mov.total_produzido,
                'quantidade_atual': produto.quantidade
            })
    
    return jsonify({
        'titulo': 'Produtos em Produção',
        'produtos': relatorio,
        'total_produtos_producao': len(relatorio)
    })

