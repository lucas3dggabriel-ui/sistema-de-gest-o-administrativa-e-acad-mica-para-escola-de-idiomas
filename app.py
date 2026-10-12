from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    matricula = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    curso = db.Column(
        db.String(50),
        nullable=False
    )

    turma = db.Column(
        db.String(50),
        nullable=False
    )

    nota = db.Column(
        db.Float,
        nullable=False
    )


with app.app_context():
  db.create_all()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/api/alunos', methods=['GET', 'POST'])
def gerenciar_alunos():
  novo_aluno = Aluno(
    matricula=dados['matricula'],
    nome=dados['nome'],
    curso=dados['curso'],
    turma=dados['turma'],
    nota=dados['nota']
)
  db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201

  alunos = Aluno.query.all()
  resultado = [{
    'id': a.id,
    'matricula': a.matricula,
    'nome': a.nome,
    'curso': a.curso,
    'turma': a.turma,
    'nota': a.nota
} for a in alunos]
  return jsonify(resultado)


@app.route('/api/taxa-cambio')
def taxa_cambio():
  url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL'
  resposta = requests.get(url).json()
  return jsonify(resposta)


@app.route('/api/analise-notas')
def analise_notas():
  alunos = Aluno.query.all()
  if not alunos:
    return jsonify({'media_geral': 0, 'total_alunos': 0})
  df = pd.DataFrame([{'nota': a.nota} for a in alunos])
  media_geral = float(df['nota'].mean())
  return jsonify({'media_geral': media_geral, 'total_alunos': len(df)})

@app.route('/api/alunos/<int:id>', methods=['DELETE'])
def excluir_aluno(id):

    aluno = Aluno.query.get(id)

    if not aluno:
        return jsonify({
            'erro': 'Aluno não encontrado'
        }), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({
        'mensagem': 'Aluno removido com sucesso'
    })


@app.route('/api/dashboard')
def dashboard():

    alunos = Aluno.query.all()

    total_alunos = len(alunos)

    media_notas = (
        sum(aluno.nota for aluno in alunos) / total_alunos
        if total_alunos > 0 else 0
    )

    return jsonify({
        'total_alunos': total_alunos,
        'media_notas': round(media_notas, 2)
    })


if __name__ == '__main__':
    app.run(debug=True)