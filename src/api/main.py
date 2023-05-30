from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nlp.Embeddings_model import Transformer
from integracion_solr import solr_client
import requests as r
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import numpy as np

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
SOLR_CORE_GRUPOS = 'grupos/'
SOLR_CORE_INVESTIGADORES = 'investigadores/'

ID_CHARS = "!\"#$%&'()[]*+.-/:;<=>?@[\]^`{|}~"

modelo_embeddings = Transformer()

@app.get('/')
async def docs():
    response = RedirectResponse('docs')
    return response

#Take string, split it and return dictionary
def util_format(string_array,name):
    new_dict = string_array.split(';')
    return {'id':new_dict[0],name:new_dict[1]}

def get_array_dict(list_items,name):
    list_dict = []
    for l in list_items:
        list_dict.append(util_format(l,name))
    return list_dict

def validate_input(input):
    if input.isspace() or input in ID_CHARS or input =='*':
        return False
    return True

def format_query(query):
    return '\"'+query.lower()+'\"'


def fill_topk_values(topk):
    for item in topk:
        doc = solr_client.get_project_by_id(item.get('id')).get('docs')[0]
        item['propuesta']  = doc.get('propuesta')
        item['estado']  = doc.get('estado')
        item['fecha_inicio'] =  doc.get('fecha_inicio')
        item['fecha_fin'] = doc.get('fecha_fin')
        item['grupo'] = doc.get('grupo')
        item['miembros'] = doc.get('miembros')
        item['descripcion'] = doc.get('descripcion')
        item['obj_general'] = doc.get('obj_general')
        item['obj_especifico'] = doc.get('obj_especifico')
        item['metodologia'] = doc.get('metodologia')
        item['pertinencia'] = doc.get('pertinencia')
        item['comunidades'] = doc.get('comunidades')
        item['sujeto_investigacion'] = doc.get('sujeto_investigacion')
        item['ubicaciones'] = doc.get('ubicaciones')
    return topk

def remove_duplicates_knn(results,top10):
    print(f'original size {len(results)}')
    for item in top10:
        for result in results:
           #id1 = item.get('id')
            #id2 = result.get('id')
            #print(f'{id1} {id2}')
            if item.get('id') == result.get('id'):
                #print('equal, deleting')
                results.remove(result)
                #$print(f'new size {len(results)}')
               # print('ESTAAAA')
    return results


def filter_knn_response(doc_vector,propuesta='',estado='',comunidades='sin_comunidades'):
    filtered_doc = []

    for doc in doc_vector:
        prop_doc = doc.get('propuesta')
        estado_doc = doc.get('estado')
        com_doc = doc.get('comunidades')
        prop_filter = ''
        estado_filter = ''
        com_filter = ''
        #print(f'propuesta doc {prop_doc} propuesta filtro {propuesta}')
        if not propuesta:
            prop_filter = prop_doc
        else:
            prop_filter = propuesta[1:-1]
        if not estado:
            estado_filter = estado_doc
        else:
            estado_filter = estado[1:-1]
        if comunidades == 'sin_filtrar':
            com_filter = com_doc
        elif comunidades == 'sin_comunidades':
            com_filter = ['NAN']
        elif comunidades == 'con_comunidades':
            if com_doc != ['NAN']:
                com_filter == com_doc
            else:
                com_filter = []
        print('doc')
        print(f'prop {prop_doc} estado {estado_doc} comunidades {com_doc}')
        print('filter')
        print(f'prop {prop_filter} estado {estado_filter} comunidades {com_filter}')
        if prop_filter == prop_doc and estado_filter == estado_doc and com_filter == com_doc:
            print('filtering')
            #print(doc)
            filtered_doc.append(doc)             
    return filtered_doc

def make_knn_query(vector, topk,propuesta ='',estado='',comunidades='sin_filtrar'):
    doc_vector = solr_client.get_knn_results(vector,topk)
    ###get the details so we can filter this response
    doc_vector = fill_topk_values(doc_vector)
    ##Need to filter this response (len should be topk)
    print(f'len before filtering {len(doc_vector)}')
    doc_vector = filter_knn_response(doc_vector,propuesta,estado,comunidades)
    print(f'len after filtering {len(doc_vector)}')
    return doc_vector

def get_general_results(query,num,inicio,propuesta,estado,comunidades):
    response = solr_client.get_projects_results(query,3000,0,propuesta,estado,comunidades)
    found = response.get('numFound')
    docs = solr_client.get_projects_results(query,found,0,propuesta,estado,comunidades).get('docs')
    return docs


"""
ENDPOINT: /search/proyectos/topk/{query}.
ARGUMENTOS:
    - query:string =  termino de busqueda
RETORNO: 
    - Response con los 10 proyectos mas similares al embedding generado por el termino de busqueda
"""
@app.get('/search/proyectos/topk/{query}')   
async def search_proyectos_topk(query, num=10, inicio=0):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        vector = modelo_embeddings.embed(query)
        docs = solr_client.get_knn_results(vector,20)
        print('RESULTADOS VECTORIAL')
        print(docs)
        return docs[10:len(docs)]

@app.get('/search/proyectos/{titulo}/topk')   
async def search_proyectos_titulo_topk(query, num=10, inicio=0):
    if query.isspace() or query =='*':
        return 'No se encontraron resultados para la busqueda'
    else:
        vector = modelo_embeddings.embed(query)
        docs = solr_client.get_knn_results(vector,11)
        docs.pop(0)
        return docs


@app.get('/search/proyectos/{query}')   
async def search_proyectos(query, num=10, inicio=0,propuesta = '', estado='',comunidades='sin_filtrar'):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_projects_results(query,3000,inicio,propuesta,estado,comunidades)
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10,propuesta,estado,comunidades)
        
        #print(docs_vector)
        print(f'INICIOOOO {type(inicio)}')
        if(response.get('numFound')>0):
            docs = get_general_results(query,num,inicio,propuesta,estado,comunidades)
            docs = remove_duplicates_knn(docs,docs_vector)    
            print(f'LEN OF DOCS: {len(docs)} LEN OF KNN: {len(docs_vector)}')
            docs = docs = docs_vector+docs            
            for doc in docs:
                #doc['grupo'] = get_array_dict(doc['grupo'],'nombre')
                if(doc['grupo'][0] != 'No asociado a grupos'):
                    #print(doc['grupo'])
                    doc['grupo'] = get_array_dict(doc['grupo'],'nombre')
            lower = int(inicio)
            upper = int(inicio)+int(num)
            sublist = docs[lower:upper]
            print(f'LEN OF DOCS: {len(docs)} LOWER {lower} UPPER {upper} NEWLEN {len(sublist)}')
            return docs[lower:upper]
        else:
            return docs_vector


"""
ENDPOINT: /proyectos/{id}.
ARGUMENTOS:
    - id:string =  id del documento
RETORNO: 
    - Response con los parametros del proyecto de investigacion correspondiente al ID de entrada
"""
@app.get('/proyectos/{id}')   
async def proyectos(id):
    if id.isspace() or id in ID_CHARS:
        return None
    else:
        response = solr_client.get_project_by_id(id)
        print(response)
        if(response.get('numFound')>0):
            doc = response.get('docs')[0]
            doc['miembros'] = get_array_dict(doc['miembros'],'nombre')
            #doc['grupo'] = get_array_dict(doc['grupo'],'nombre')
            print(doc['grupo'])
            if(doc['grupo'][0] != 'No asociado a grupos'):
                    print(doc['grupo'])
                    doc['grupo'] = get_array_dict(doc['grupo'],'nombre')
            return doc
        else:
            return []

"""
ENDPOINT: /search/proyectos/coordinates/{query}.
ARGUMENTOS:
    - query:string =  consulta a ingresar
RETORNO: 
    - Response con la lista de todas las ubicaciones identificadas para la consulta
"""
@app.get('/search/proyectos/coordinates/{query}')
async def search_proyectos_coordinates(query):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_projects_results(query,2000,0,args ='ubicacion')
        docs = response.get('docs')
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10)
        docs = remove_duplicates_knn(docs,docs_vector)    
        docs = docs_vector+docs
        coordinates = []
        for doc in docs:
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
    if query.isspace() or query in ID_CHARS:
        return []
    else:
    #La eliminacion de stopwords deberia realizarse durante la fase de indexado de informacion, esto es temporal
        query = format_query(query)
        stopwords = open('stopwords.txt').readlines()
        stopwords = [word.strip() for word in stopwords]        
        response = solr_client.get_projects_results(query,2000,0,args ='comunidad')                
        docs = response.get('docs')
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10)
        print(f'LENLENLEN {len(docs_vector)}') 
        docs = docs_vector+docs
        communities_resp = []
        for doc in docs:        
            communities_doc = doc.get('comunidades')        
            for com in communities_doc:
                com_split = com.split(' ')            
                for word in com_split:
                    if word.lower()  not in stopwords and word.isnumeric()==False and len(word)>2 and word:
                        communities_resp.append(word.lower())       
        word_cloud =[]
        
        df_test = pd.DataFrame(pd.value_counts(np.array(communities_resp)))        
        for index,row in df_test.iterrows():
            #val_normalized = (int(row[0]) - 1) / (205 - 1) * (5 - 1) + 1
            word_cloud.append({'text':index,'value':1})
        print(word_cloud)
        return word_cloud


"""
ENDPOINT: /search/proyectos/{query}/total.
ARGUMENTOS:
    - id:string =  id del documento
RETORNO: 
    - Response con los parametros del proyecto de investigacion correspondiente al ID de entrada
"""
@app.get('/proyectos/{query}/total')   
async def proyectos_total(query,propuesta = '', estado='',comunidades='sin_filtrar'):
    query = format_query(query)
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        #response = solr_client.get_projects_results(query,10,0,propuesta,estado,comunidades)
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10,propuesta,estado,comunidades)
        docs = get_general_results(query,10,0,propuesta,estado,comunidades)
        docs = remove_duplicates_knn(docs,docs_vector)    
        docs = docs = docs_vector+docs
        return len(docs)



#### Group Queries
@app.get('/search/grupos/{query}')   
async def search_grupos(query,num=10, inicio=0):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_groups_results(query,num,inicio)
        if(response.get('numFound')>0):
            docs = response.get('docs')
            print(docs)
            return docs
        else:
            return []


@app.get('/grupos/{id}')   
async def grupos(id):
    if id.isspace() or id in ID_CHARS:
        return None
    else:
        response = solr_client.get_group_by_id(id)
        if(response.get('numFound')>0):
            doc = response.get('docs')[0]
            doc['proyectos'] = get_array_dict(doc['proyectos'],'titulo')
            doc['investigadores'] = get_array_dict(doc['investigadores'],'nombre')
            return response
        else:
            return []

@app.get('/grupos/{query}/total')   
async def grupos_total(query):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_groups_results(query)
        return response.get('numFound')


#### Researchers Queries


@app.get('/search/investigadores/{query}')   
async def search_investigadores(query,num=10, inicio=0):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_researchers_results(query,num,inicio)
        if(response.get('numFound')>0):
            docs = response.get('docs')
            return docs
        else:
            return []


@app.get('/investigadores/{id}')   
async def investigadores(id):
    if id.isspace() or id in ID_CHARS:
        return None
    else:
        response = solr_client.get_researcher_by_id(id)
        if(response.get('numFound')>0):
            doc = response.get('docs')[0]
            doc['proyectos'] = get_array_dict(doc['proyectos'],'titulo')
            doc['grupos'] = get_array_dict(doc['grupos'],'nombre')
            print(type(doc))
            return doc
        else:
            return []


@app.get('/investigadores/{query}/total')   
async def investigadores_total(query):
    if query.isspace() or query in ID_CHARS:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_researchers_results(query,10,0)
        return response.get('numFound')
    
    