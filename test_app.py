from app import app, db, Aluno
import pytest


@pytest.fixture
def client():

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:

        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_index(client):

    response = client.get('/')

    assert response.status_code == 200


def test_adicionar_aluno(client):

    response = client.post(
        '/api/alunos',
        json={
            'nome': 'Carlos Silva',
            'curso': 'Espanhol',
            'nota': 8.8
        }
    )

    assert response.status_code == 201


def test_listar_alunos(client):

    client.post(
        '/api/alunos',
        json={
            'nome': 'Carlos Silva',
            'curso': 'Espanhol',
            'nota': 8.8
        }
    )

    response = client.get('/api/alunos')

    assert response.status_code == 200

    dados = response.get_json()

    assert len(dados) >= 1


def test_dashboard(client):

    client.post(
        '/api/alunos',
        json={
            'nome': 'Ana',
            'curso': 'Inglês',
            'nota': 10
        }
    )

    response = client.get('/api/dashboard')

    assert response.status_code == 200

    dados = response.get_json()

    assert dados['total_alunos'] >= 1


def test_excluir_aluno(client):

    client.post(
        '/api/alunos',
        json={
            'nome': 'Pedro',
            'curso': 'Francês',
            'nota': 9
        }
    )

    response = client.get('/api/alunos')

    aluno_id = response.get_json()[0]['id']

    delete = client.delete(f'/api/alunos/{aluno_id}')

    assert delete.status_code == 200
