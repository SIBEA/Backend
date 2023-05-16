from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nlp.embeddings import embed
import requests as r
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

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
Este endpoint retorna los top 10 proyectos de investigacion a partir de la busqueda
"""
@app.get('/search/proyectos/topk,{query}')   
async def search_proyectos_topk(query, num=10, inicio=0):
    vector = embed(query)
    SOLR_QUERY = 'select?q={!knn f=vector topK=10}'+str(vector.tolist())
    SOLR_QUERY_ARGS = '&fl=title'
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio    
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    #print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

"""
Este endpoint se encarga de retornar los resultados generales para los proyectos
"""
@app.get('/search/proyectos,{query}')   
async def search_proyectos_general(query, num=10, inicio=0):
    SOLR_QUERY = 'select?q=title:'+query+' or descripcion:'+query
    SOLR_QUERY_ARGS = '&fl=title, descripcion,grupo, comunidades'
    vector = embed(query)
    SOLR_QUERY_RERANK = '&rq={!rerank reRankQuery=$rqq reRankWeight=1}&rqq={!knn f=vector topK=50}'+str(vector.tolist())
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio
    #vector = embed(query)
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_RERANK+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

"""
Este endpoint se encarga de retornar los resultados generales para los proyectos, NO HACE RERANKING, SOLO EXISTE PARA PRUEBAS
"""
@app.get('/search/proyectos/norerank,{query}')   
async def search_proyectos_general_norerank(query, num=10, inicio=0):
    SOLR_QUERY = 'select?q=title:'+query+' or descripcion:'+query
    SOLR_QUERY_ARGS = '&fl=title, descripcion,grupo, comunidades'
    #vector = embed(query)
    #SOLR_QUERY_RERANK = 'rq={!rerank reRankQuery=$rqq reRankWeight=1}&rqq={!knn f=vector topK=50}'+str(vector.tolist())
    SOLR_QUERY_PAG = '&rows='+num+'&start='+inicio
    #vector = embed(query)
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

"""
TODO: 
Endpoint Coordenadas
Endpoint Comunidades
Endpoint Grupos
Endpoint Investigadores
"""
