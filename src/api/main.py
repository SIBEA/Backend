from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nlp.embeddings import embed
import requests as r
from enum import Enum
app = FastAPI()

 
class Models(Enum):
    def __str__(self):
        return str(self.value)
    model_minilm='model_minilm'
    model_mpnet='model_mpnet'
    model_multilingual_distiluse_v1='model_multilingual_distiluse_v1'
    model_multilingual_distiluse_v2='model_multilingual_distiluse_v2'
    model_multilingual_minilm='model_multilingual_minilm'
    model_multilingual_mpnet='model_multilingual_mpnet'

class Method(Enum):
    def __str__(self):
        return str(self.value)
    dot_product = '_dot'
    cosine = '_cosine'
    euclidean = '_euclidean'


SOLR_URL = 'http://solr:8983/solr/'
SOLR_QUERY = 'query?q={!knn%20f=vector%20topK=50}'
SOLR_QUERY_ARGS = '&fl=titulo,facultad,departamento,objetivos,resumen&rows=100'
@app.get('/')
async def docs():
    response = RedirectResponse('docs')
    return response

@app.get('/search/{model},{query},{method}')   
async def search_v1(query,model:Models,method:Method,percentage = 0):
    SOLR_METHOD = str(method)
    SOLR_CORE = str(model)+SOLR_METHOD+'/'
    vector = embed(query,str(model))
    q1 = '&q_vector={!knn%20f=vector%20topK=50}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
    req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+q1+SOLR_QUERY_ARGS
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    return response

