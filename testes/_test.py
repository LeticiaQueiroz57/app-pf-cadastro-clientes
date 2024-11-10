import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from src.services import userService
from main import app
from mongomock import MongoClient
from src.models import userModel

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_database():
    
    mock_client = MongoClient()
    userService.Usuario = mock_client.db.Usuario
    yield
    mock_client.close()

def test_criar_dados_com_email_invalido():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "email_invalido",  
        "telefone": "123456789",
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'msg' in response.json()['detail'][0]
    assert 'Value error' in response.json()['detail'][0]['msg']


def test_criar_dados_com_telefone_invalido():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "invalid_phone",  
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  

    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'msg' in response.json()['detail'][0]
    assert 'Value error' in response.json()['detail'][0]['msg']


def test_criar_dados_com_preco_negativo():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "123456789",
        "preco": -50.0  
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'msg' in response.json()['detail'][0]
    assert 'O preço deve ser positivo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_nome_vazio():
    payload = {
        "nome": "",  
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "123456789",
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'nome não pode ser nulo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_sobrenome_vazio():
    payload = {
        "nome": "John",
        "sobrenome": "",  
        "email": "john.doe@example.com",  
        "telefone": "123456789",
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'sobrenome não pode ser nulo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_telefone_vazio():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "", 
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    

    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'telefone não pode ser nulo' in response.json()['detail'][0]['msg']



def test_criar_dados_com_sobrenome_vazio():
    payload = {
        "nome": "John",
        "sobrenome": "",  
        "email": "john.doe@example.com",  
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'sobrenome não pode ser nulo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_nome_vazio():
    payload = {
        "nome": "",  
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "123456789",
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'nome não pode ser nulo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_preco_zero():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "123456789",
        "preco": 0.0  
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  #
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'O preço deve ser positivo' in response.json()['detail'][0]['msg']


def test_criar_dados_com_telefone_vazio():
    payload = {
        "nome": "John",
        "sobrenome": "Doe",
        "email": "john.doe@example.com",  
        "telefone": "",  
        "preco": 100.0
    }
    response = client.post("/user/criar", json=payload)
    assert response.status_code == 422  
    
    
    assert 'detail' in response.json()
    assert len(response.json()['detail']) == 1
    assert response.json()['detail'][0]['loc'] == ['body']
    assert 'Value error' in response.json()['detail'][0]['msg']
    assert 'telefone não pode ser nulo' in response.json()['detail'][0]['msg']