from flask import Flask, send_from_directory
import requests as r
import json
from flask_restx import Api, Resource
from nlp.embeddings import embed

##TEMPORAL, MIGRAR A FASTAPI
app = Flask(__name__)
api = Api(app)




SOLR_URL = 'http://localhost:8983/solr/'
SOLR_QUERY = 'query?q={!knn%20f=vector%20topK=50}'
SOLR_QUERY_ARGS = '&fl=titulo,facultad,departamento,resumen&rows=100'

#Lista de endpoints (Cada endpoint expone comunicacion a un core de solr, el cual contiene documentos vectorizados usando el modelo en el nombre del core)

#'model_minilm'
#'model_mpnet'
#'model_multilingual_distiluse_v1'
#'model_multilingual_distiluse_v2'
#'model_multilingual_minilm'


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#Considerar descartar, no da buenos resultados#Considerar descartar, no da buenos resultados
@api.doc(params={'query': 'Consulta para el modelo'})
@api.route('/model_minilm/<query>,<percentage>')
class Query(Resource):
    
    def get(self,query,percentage):
        SOLR_CORE = 'model_minilm/'
        vector = embed(query,'model_minilm')
        #q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
        #print(response.json())
        return response

#Considerar descartar, no da buenos resultados
@api.route('/model_mpnet/<query>,<percentage>')
class Query(Resource):
    
    def get(self,query,percentage):
        vector = embed(query,'model_mpnet')
        SOLR_CORE = 'model_mpnet/'
       # q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
        #print(response.json())
        return response

##Da buenos resultados
@api.route('/model_multilingual_distiluse_v1/<query>,<percentage>')
class Query(Resource):
    
    def get(self,query,percentage):
        SOLR_CORE = 'model_multilingual_distiluse_v1/'
        vector = embed(query,'model_multilingual_distiluse_v1')
        #q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
        #print(response.json())
        return response


##Da buenos resultados
@api.route('/model_multilingual_distiluse_v2/<query>,<percentage>')
class Query(Resource):    
    def get(self,query,percentage):
        SOLR_CORE = 'model_multilingual_distiluse_v2/'        
        vector = embed(query,'model_multilingual_distiluse_v2')
        #q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
        #print(response.json())
        return response
    

##Resultados no tan aceptables
@api.route('/model_multilingual_minilm/<query>,<percentage>')
class Query(Resource):
    def get(self,query,percentage):
        SOLR_CORE = 'model_multilingual_minilm/'
        vector = embed(query,'model_multilingual_minilm')

       # q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
        #print(response.json())
        return response
    

##Da resultados Aceptables
@api.route('/model_multilingual_mpnet/<query>,<percentage>')
class Query(Resource):        
    def get(self,query,percentage):
        SOLR_CORE = 'model_multilingual_mpnet/'
        vector = embed(query,'model_multilingual_mpnet')
       # q1 = '&q_vector={!knn%20f=vector%20topK=100}'+str(vector.tolist())+'&fq={!frange%20l='+percentage+'}$q_vector'
        req = SOLR_URL+SOLR_CORE+SOLR_QUERY+str(vector.tolist())+SOLR_QUERY_ARGS
        print(req)
        response = r.get(req).json()
        del response["responseHeader"]["params"]
            #print(response.json())
        return response
    
    
if __name__ == '__main__':
    app.run(debug = True)
