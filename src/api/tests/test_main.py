from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app=app)


def test_topk():   
    query = 'Paciente'
    response = client.get('/search/proyectos/topk/'+query)
    assert response.status_code == status.HTTP_200_OK


def test_topk_titulo():   
    query = 'Paciente'
    response = client.get('/search/proyectos/'+query)
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_general():   
    query = 'Paciente'
    response = client.get('/search/proyectos/'+query+'?num=10&inicio=0&comunidades=sin_filtrar')
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_general_filtro():   
    query = 'Paciente'
    response = client.get('/search/proyectos/'+query+'?num=10&inicio=0&comunidades=con_comunidades')
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_id():   
    id = 'P_001149'
    response = client.get('/proyectos/'+id)
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_coordinates():   
    query = 'Paciente'
    response = client.get('/search/proyectos/coordinates'+query)
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_communities():   
    query = 'Paciente'
    response = client.get('/search/proyectos/communities'+query)
    assert response.status_code == status.HTTP_200_OK

def test_proyectos_total():   
    query = 'Paciente'
    response = client.get('/proyectos/'+query+'/total?&comunidades=con_comunidades')
    assert response.status_code == status.HTTP_200_OK

def test_grupos_general():   
    query = 'Paciente'
    response = client.get('/search/grupos/'+query+'?num=10&inicio=0')
    assert response.status_code == status.HTTP_200_OK

def test_grupos_id():   
    id = 'G_00108'
    response = client.get('/grupos/'+id)
    assert response.status_code == status.HTTP_200_OK

def test_grupos_total():   
    query = 'Paciente'
    response = client.get('/grupos/'+query+'/total')
    assert response.status_code == status.HTTP_200_OK

def test_investigadores_general():   
    query = 'Paciente'
    response = client.get('/search/investigadores/'+query+'?num=10&inicio=0')
    assert response.status_code == status.HTTP_200_OK

def test_investigadores_total():   
    query = 'Paciente'
    response = client.get('/investigadores/'+query+'/total')
    assert response.status_code == status.HTTP_200_OK

def test_grupos_id():   
    id = 'I_001269'
    response = client.get('/investigadores/'+id)
    assert response.status_code == status.HTTP_200_OK




def test_topk_fail():   
    query = '*'
    response = client.get('/search/proyectos/topk/'+query)
    assert response.json()==[]


def test_topk_titulo_fail():   
    query = '*'
    response = client.get('/search/proyectos/'+query)
    assert response.json()==[]

def test_proyectos_general_fail():   
    query = '*'
    response = client.get('/search/proyectos/'+query+'?num=10&inicio=0&comunidades=sin_filtrar')
    assert response.json()==[]

def test_proyectos_general_filtro_fail():   
    query = '*'
    response = client.get('/search/proyectos/'+query+'?num=10&inicio=0&comunidades=con_comunidades')
    assert response.json()==[]

def test_proyectos_id_fail():   
    id = '*'
    response = client.get('/proyectos/'+id)
    assert response.json()==None

def test_proyectos_coordinates_fail():   
    query = '*'
    response = client.get('/search/proyectos/coordinates'+query)
    assert response.json()==[]

def test_proyectos_total_fail():   
    query = '*'
    response = client.get('/proyectos/'+query+'/total?&comunidades=con_comunidades')
    assert response.json()==[]

def test_grupos_general_fail():   
    query = '*'
    response = client.get('/search/grupos/'+query+'?num=10&inicio=0')
    assert response.json()==[]

def test_grupos_id_fail():   
    id = '*'
    response = client.get('/grupos/'+id)
    assert response.json()==[]

def test_grupos_total_fail():   
    query = '*'
    response = client.get('/grupos/'+query+'/total')
    assert response.json()==[]

def test_investigadores_general_fail():   
    query = '*'
    response = client.get('/search/investigadores/'+query+'?num=10&inicio=0')
    assert response.json()==[]

def test_investigadores_total_fail():   
    query = '*'
    response = client.get('/investigadores/'+query+'/total')
    assert response.json()==[]

def test_grupos_id_fail():   
    id = '*'
    response = client.get('/investigadores/'+id)
    assert response.json()==None
