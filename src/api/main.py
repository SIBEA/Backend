from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nlp.Embeddings_model import Transformer
from integracion_solr import solr_client
import requests as r
from fastapi import Request
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import io
import pandas as pd
import numpy as np
import re 

from datetime import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
 
SOLR_URL = 'http://solr:8983/solr/'
SOLR_CORE_PROYECTOS = 'proyectos/'
SOLR_CORE_GRUPOS = 'grupos/'
SOLR_CORE_INVESTIGADORES = 'investigadores/'

ID_CHARS =  r"[!\"#$%&'()\[\]+./:;<\'=>?@\\^`{|}~]"

modelo_embeddings = Transformer()

@app.get('/')
async def docs():
    response = RedirectResponse('docs')
    return response

#Utility methods

def util_format(string_array,name):
    new_dict = string_array.split(';')
    return {'id':new_dict[0],name:new_dict[1]}

def get_array_dict(list_items,name):
    list_dict = []
    for l in list_items:
        list_dict.append(util_format(l,name))
    return list_dict

def validate_input(input):
    if re.search(ID_CHARS, input):
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
            if item.get('id') == result.get('id'):
                results.remove(result)
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
        if comunidades == 'sin_comunidades':
            com_filter = ['NAN']
        elif comunidades == 'con_comunidades':
            if com_doc != ['NAN']:
                com_filter == com_doc
            else:
                com_filter = []
        else:
            com_filter = com_doc
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

# Projects endpoints

"""
ENDPOINT: /search/proyectos/topk/{query}.
ARGUMENTOS:
    - query:string =  termino de busqueda
RETORNO: 
    - Response con los 10 proyectos mas similares al embedding generado por el termino de busqueda
"""
@app.get('/search/proyectos/topk/{query}')   
async def search_proyectos_topk(query, num=10, inicio=0):
    if validate_input(query) == False:
        return []
    else:
        vector = modelo_embeddings.embed(query)
        docs = solr_client.get_knn_results(vector,20)
        print('RESULTADOS VECTORIAL')
        #print(docs)
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
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_projects_results(query,3000,inicio,propuesta,estado,comunidades)
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10,propuesta,estado,comunidades)
        
        #print(docs_vector)
        found = response.get('numFound')
        print(f'RESPONSE NUMFOUND: {found}')
        print(f'INICIOOOO {type(inicio)}')
        if(response.get('numFound')>0):
            docs = get_general_results(query,num,inicio,propuesta,estado,comunidades)
            print('BEFORE REMOVING DUPLICATES')
            print(f'LEN OF DOCS: {len(docs)} LEN OF KNN: {len(docs_vector)}')
            docs = remove_duplicates_knn(docs,docs_vector)    
            print('AFTER REMOVING DUPLICATES')
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
            #print(doc['grupo'])
            if(doc['grupo'][0] != 'No asociado a grupos'):
                    #print(doc['grupo'])
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
    print('LKAISHAKWLSJHLKAJSH')
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        print('LKAISHAKWLSJHLKAJSH')
        response = solr_client.get_projects_results(query,2000,0,args ='ubicacion')
        print('LENGTH')
        print(response.get('numFound'))
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
    if validate_input(query) == False:
        return []
    else:
    #La eliminacion de stopwords deberia realizarse durante la fase de indexado de informacion, esto es temporal
        query = format_query(query)
        stopwords = open('stopwords.txt').readlines()
        stopwords = [word.strip() for word in stopwords]        
        response = solr_client.get_projects_results(query,2000,0,args ='comunidad')                
        docs = response.get('docs')
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10,comunidades = 'con_comunidades')
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
    print("TOTAL")
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        #response = solr_client.get_projects_results(query,10,0,propuesta,estado,comunidades)
        vector = modelo_embeddings.embed(query)
        docs_vector = make_knn_query(vector,10,propuesta,estado,comunidades)
        print("PETICION A SOLR")
        docs = get_general_results(query,10,0,propuesta,estado,comunidades)
        docs = remove_duplicates_knn(docs,docs_vector)    
        docs = docs = docs_vector+docs
        
        return len(docs)
    
"""
ENDPOINT: reports/locations/
ARGUMENTOS:
    - fecha inicial:
    - fecha final
Retorno:
    - Response con un CSV que contenga los proyectos que tengan ubicaciones en estas fechas.
"""

"""
1. Query projects for all projects that contain locations.
2. select only those within the dates given.
3. Create a CSV file from the data returned (dataframe most likely)
"""
def format_date(date):
    return date.split("T")[0]

def format_location(location):
    return location.split(";")

def clean_solr_string(element, chars):
    translation_table = str.maketrans('', '', chars)
    return element.translate(translation_table)


def validar_fecha(fecha_inicio, fecha_fin, fecha_inicio_proyecto, fecha_fin_proyecto):
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_inicio_proyecto = datetime.strptime(fecha_inicio_proyecto, '%Y-%m-%d')
        fecha_fin_proyecto = datetime.strptime(fecha_fin_proyecto, '%Y-%m-%d')

        print("----------------")
        print(fecha_inicio)
        print(fecha_fin)
        print(fecha_inicio_proyecto)
        print(fecha_fin_proyecto)
        print("----------------")
        
        #return not (fecha_fin < fecha_inicio_proyecto or fecha_inicio > fecha_fin_proyecto)
        return fecha_inicio<=fecha_inicio_proyecto<=fecha_fin or fecha_inicio<=fecha_fin_proyecto<=fecha_fin

    except ValueError:
        print("UPS")
        return False

"""
id
titulo
fecha_inicio
fecha_fin
ubicaciones

"""

"http://localhost:8000/generate_csv/%20method=?fecha_inicio=2023-07-23&fecha_fin=2023-07-23"
"http://localhost:8000/generate_csv/?fecha_inicio=2010-01-01&fecha_fin=2040-01-01"
#testing how to download a csv
@app.get('/reporte_fechas/')
async def create_report_dates(fecha_inicio , fecha_fin ):
    dict_response = solr_client.get_projects_results("\"*\"",3000,0,args ='report_location')    
    # filter projects within range
    proyectos = []
    for dict in dict_response.get("docs"):   
        dict["titulo"] = clean_solr_string(dict["titulo"][0],"[]\'")
        dict["fecha_inicio"] = format_date(dict["fecha_inicio"][0])
        dict["fecha_fin"] = format_date(dict["fecha_fin"][0])
        dict["ubicaciones"] = format_location(dict["ubicaciones"][0])        
        if validar_fecha(fecha_inicio,fecha_fin,dict["fecha_inicio"],dict["fecha_fin"]) == True:
            print("VALIDATED")
            proyectos.append({
                "id":dict["id"],
                "titulo":dict["titulo"],
                "ubicacion":dict["ubicaciones"][0],
                "latitud":dict["ubicaciones"][1],
                "longitud":dict["ubicaciones"][2],
                "fecha_inicio":dict["fecha_inicio"],
                "fecha_fin":dict["fecha_fin"]
            })
    print(proyectos)
    # append said projects into a csv
    df_locations = pd.DataFrame(proyectos)
    #df_locations.to_csv("./test.csv")
    # download the file
    stream = io.StringIO()
    df_locations.to_csv(stream, index=False)
    current_date_time = datetime.now()
    filename = "Reporte ubicaciones "+str(current_date_time)+".csv"
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response

"""
FORMS FOR THE DATE FUNCTION
"""

@app.get("/reporte_ubicaciones/")
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Group Endpoints

@app.get('/search/grupos/{query}')   
async def search_grupos(query,num=10, inicio=0):
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_groups_results(query,num,inicio)
        if(response.get('numFound')>0):
            docs = response.get('docs')
            #print(docs)
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
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_groups_results(query)
        return response.get('numFound')


# Researchers Endpoints

@app.get('/search/investigadores/{query}')   
async def search_investigadores(query,num=10, inicio=0):
    if validate_input(query) == False:
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
    if validate_input(query) == False:
        return []
    else:
        query = format_query(query)
        response = solr_client.get_researchers_results(query,10,0)
        return response.get('numFound')
    
    