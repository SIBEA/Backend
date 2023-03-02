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


SOLR_URL = 'http://localhost:8983/solr/'
SOLR_QUERY = 'query?q={!knn%20f=vector%20topK=50}'
SOLR_QUERY_ARGS = '&fl=titulo,facultad,departamento,resumen&rows=100'
@app.get('/')
async def docs():
    response = RedirectResponse('docs')
    return response

@app.get('/search/{model},{query}')   
async def search_v1(query,model:Models):
    print(str(model))
    #SOLR_CORE = 'model_multilingual_distiluse_v1/'
    SOLR_CORE = str(model)+'/'
    #vector = embed(query,'model_multilingual_distiluse_v1')
    vector = embed(query,str(model))
    #q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
    req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
    print(req)
    response = r.get(req).json()
    del response["responseHeader"]["params"]
    #response["model"]=model
    #print(response.json())
    return response

