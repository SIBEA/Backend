from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nlp.embeddings import embed
import requests as r
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import numpy as np


"""
Checklist
Endpoint general - Functional
Endpoint topK - Functional
Endpoint Coordenadas - Get all coordinates and return a list [Needs to be polished but its functional]
Endpoint Comunidades - Get all communities and return a list [Needs to be polished but its functional]
Endpoint Grupo particular - TODO
Endpoint Investigador particular - TODO
Endpoint Grupos -TODO
Endpoint Investigadores - TODO
Integrar Locust (definirlo en requirements.txt) - TODO 
Definir pruebas de carga con Locust - TODO
Realizar pruebas de endpoints con TestClient - TODO
"""


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
SOLR_URL = 'http://solr:8983/solr/'
SOLR_CORE_PROYECTOS = 'proyectos/'
#SOLR_CORE_GRUPOS = 'grupos'
#SOLR_CORE_INVESTIGADORES = 'investigadores'

@app.get('/')
async def docs():
    response = RedirectResponse('docs')
    return response

"""
ENDPOINT: /search/proyectos/topk/{query}.
ARGUMENTOS:
    - query:string =  termino de busqueda
RETORNO: 
    - Response con los 10 proyectos mas similares al embedding generado por el termino de busqueda
"""
@app.get('/search/proyectos/topk/{query}')   
async def search_proyectos_topk(query, num=10, inicio=0):
    vector = embed(query)
    SOLR_QUERY = 'select?q={!knn f=vector topK=10}'+str(vector.tolist())
    SOLR_QUERY_ARGS = '&fl=id,titulo'
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio    
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

"""
ENDPOINT: /search/proyectos/{query}.
ARGUMENTOS:
    - query:string =  termino de busqueda
RETORNO: 
    - Response con la lista de resultados de busqueda
DESCRIPCION:
     Este endpoint entrega resultados de los proyectos buscando el termino ingresado en los siguientes campos:
        - titulo
        - descripcion
        - grupo
        - miembros
        - descripcion
        - obj_general
        - obj_especifico
        - metodologia
        - pertinencia
        - comunidades
        - ubicaciones
     Posteriormente reordena los resultados de busqueda (reranking) en base a la similitud del embedding generado a partir del termino de consulta
"""
@app.get('/search/proyectos/{query}')   
async def search_proyectos_general(query, num=10, inicio=0):
    SOLR_QUERY = 'select?q=titulo:'+query+' or descripcion:'+query
    SOLR_QUERY_ARGS = '&fl=id,titulo, descripcion,grupo, comunidades'
    vector = embed(query)
    SOLR_QUERY_RERANK = '&rq={!rerank reRankQuery=$rqq reRankWeight=1}&rqq={!knn f=vector topK=50}'+str(vector.tolist())
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_RERANK+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response



"""
Este endpoint se encarga de retornar los resultados generales para los proyectos, NO HACE RERANKING, SOLO EXISTE PARA PRUEBAS
"""
@app.get('/search/proyectos/norerank/{query}')   
async def search_proyectos_general_norerank(query, num=10, inicio=0):
    SOLR_QUERY = 'select?q=titulo:'+query+' or descripcion:'+query
    SOLR_QUERY_ARGS = '&fl=title, descripcion,grupo, comunidades'
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response


"""
ENDPOINT: /proyectos/{id}.
ARGUMENTOS:
    - id:string =  id del documento
RETORNO: 
    - Response con los parametros del proyecto de investigacion correspondiente al ID de entrada
"""
@app.get('/proyectos/{id}')   
async def detail_proyecto(id):
    #probar con 3903
    SOLR_QUERY = 'select?q=id:'+id
    #Definir que otros argumentos entregar o que argumentos de aqui quitar
    SOLR_QUERY_ARGS = '&fl=id,titulo, propuesta, fecha_inicio, fecha_fin, grupo, miembros, descripcion, obj_general, obj_especifico, metodologia, pertinencia, comunidades, ubicaciones'    
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

"""
ENDPOINT: /search/proyectos/coordinates/{query}.
ARGUMENTOS:
    - query:string =  consulta a ingresar
RETORNO: 
    - Response con la lista de todas las ubicaciones identificadas para la consulta
"""
@app.get('/search/proyectos/coordinates/{query}')
async def search_proyectos_coordinates(query):
    SOLR_QUERY = 'select?q=titulo:'+query+' or descripcion:'+query
    SOLR_QUERY_ARGS = '&fl=ubicaciones,titulo,id'
    SOLR_QUERY_PAG = '&rows='+str(999)
    SOLR_QUERY_REMOVE_NAN = ' and -ubicaciones:nan'
    req = req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_REMOVE_NAN+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = (r.get(req).json()).get('response')
    #Se debe implementar un modulo que gestione todo el postprocesamiento de las respuestas que entrega Solr
    print(response.keys())
    documents = response.get('docs')
    coordinates = []
    for doc in documents:
        title = doc.get('titulo')
        id = doc.get('id')
        locations = doc.get('ubicaciones')                
        for loc in locations:            
            loc = loc.split(';')
            if len(loc)>1:
                nombre = loc[0]
                lat = loc[1]
                lon = loc[2]
                coordinates.append({'id':id,'proyecto':title,'nombre':nombre,'lat':lat,'lon':lon})          
    print(coordinates)
    return coordinates

def remove_duplicates_util(locations):
    return dict.fromkeys(locations)

"""
ENDPOINT: /search/proyectos/communities/{query}.
ARGUMENTOS:
    - query:String =  consulta a ingresar
RETORNO: 
    - Response con la lista de todas las comunidades identificadas para la consulta
"""
@app.get('/search/proyectos/communities/{query}')
async def search_proyectos_communities(query):
    #La eliminacion de stopwords deberia realizarse durante la fase de indexado de informacion, esto es temporal
    stopwords = open('stopwords.txt').readlines()
    stopwords = [word.strip() for word in stopwords]
    print(f'stopwords: {stopwords}')
    SOLR_QUERY = 'select?q=titulo:'+query+' or descripcion:'+query
    SOLR_QUERY_REMOVE_NAN = ' and -comunidades:NAN'
    SOLR_QUERY_ARGS = '&fl=comunidades'
    SOLR_QUERY_PAG = '&rows='+str(999)
    req = req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_REMOVE_NAN+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = (r.get(req).json()).get('response')
    print(req)
    #Se debe implementar un modulo que gestione todo el postprocesamiento de las respuestas que entrega Solr
    documents = response.get('docs')
    communities_resp = []
    for doc in documents:        
        communities_doc = doc.get('comunidades')        
        for com in communities_doc:
            com_split = com.split(' ')            
            for word in com_split:
                if word.lower()  not in stopwords and word.isnumeric()==False and word:
                    communities_resp.append(word.lower())       
    word_cloud =[]
      
    df_test = pd.DataFrame(pd.value_counts(np.array(communities_resp)))    
    
    
    for index,row in df_test.iterrows():
        val_normalized = (int(row[0]) - 1) / (205 - 1) * (5 - 1) + 1
        word_cloud.append({'text':index,'value':val_normalized})
    print(word_cloud)
    return word_cloud



