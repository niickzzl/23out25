from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'quantidade': self.quantidade, 'preco': self.preco}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    novo = Produto(nome=data['nome'], quantidade=data['quantidade'], preco=data['preco'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Produto adicionado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    data = request.get_json()
    produto.nome = data['nome']
    produto.quantidade = data['quantidade']
    produto.preco = data['preco']
    db.session.commit()
    return jsonify({'mensagem': 'Produto atualizado!'})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto removido!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
