import requests as r


SOLR_URL = 'http://solr:8983/solr/'
SOLR_CORE_PROYECTOS = 'proyectos/'
SOLR_CORE_GRUPOS = 'grupos/'
SOLR_CORE_INVESTIGADORES = 'investigadores/'

"""
Retorna el resultado de realizar la busqueda KNN a solr
Entrada: embedding
Salida: Docs resultado del topk
"""
def get_knn_results(vector,topk):
    
    SOLR_QUERY = 'select?q={!knn f=vector topK='+str(topk)+'}'+str(vector.tolist())    
    SOLR_QUERY_FILTERS =''
    SOLR_QUERY_ARGS = '&fl=id,titulo,propuesta&rows='+str(topk)        
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_FILTERS+SOLR_QUERY_ARGS
    response = r.get(req).json().get('response')
    #print(response)
    docs = response.get('docs')
    #print(len(docs))
    return docs

def get_projects_results(query, num=10, inicio=0, propuesta = '', estado = '', comunidades = 'sin_filtrar', args = 'none'):
    SOLR_QUERY='select?defType=dismax&q='+query+' & qf=titulo + descripcion + obj_general + obj_especifico + metodologia + pertinencia + ubicaciones + comunidades + sujeto_investigacion'
    SOLR_QUERY_FILTERS =''
    if propuesta:
        print('SOLR FILTERING PROPOSAL')
        SOLR_QUERY_FILTERS+=' &fq=propuesta:'+propuesta
    if estado:
        SOLR_QUERY_FILTERS+=' &fq=estado:'+estado
    if comunidades == 'con_comunidades':
        SOLR_QUERY_FILTERS+=' &fq=-comunidades:NAN'
    if comunidades == 'sin_comunidades':
        SOLR_QUERY_FILTERS+=' &fq=comunidades:NAN'
    if args == 'comunidad':
        SOLR_QUERY_ARGS = '&fl=comunidades & fq = -comunidades:NAN'    
    elif args == 'ubicacion':
        SOLR_QUERY_ARGS = '&fl=id,titulo,ubicaciones & fq = -ubicaciones:nan'  
    else:
        SOLR_QUERY_ARGS = '&fl=id,titulo, propuesta, fecha_inicio, fecha_fin, grupo, miembros, descripcion, obj_general, obj_especifico, metodologia, pertinencia, comunidades,sujeto_investigacion, ubicaciones'

    SOLR_QUERY_PAG = '&rows='+str(num)+'&start='+str(inicio) 
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_FILTERS+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = r.get(req).json().get('response')
    #print(req)
    return response

def get_project_by_id(id):
    SOLR_QUERY = 'select?q=id:'+id
    #Definir que otros argumentos entregar o que argumentos de aqui quitar
    SOLR_QUERY_ARGS = '&fl=id,titulo,estado, propuesta, fecha_inicio, fecha_fin, grupo, miembros, descripcion, obj_general, obj_especifico, metodologia, pertinencia, comunidades,sujeto_investigacion, ubicaciones'    
    req = SOLR_URL+SOLR_CORE_PROYECTOS+SOLR_QUERY+SOLR_QUERY_ARGS
    response = r.get(req).json().get('response')
    return response

def get_groups_results(query, num=10, inicio=0):
    SOLR_QUERY='select?defType=dismax&q='+query+' & qf=nombre + proyectos + investigadores'
    SOLR_QUERY_ARGS = '&fl=id,nombre'
    SOLR_QUERY_PAG = '&rows='+str(num)+'&start='+str(inicio) 
    req = SOLR_URL+SOLR_CORE_GRUPOS+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = r.get(req).json().get('response')
    return response

def get_group_by_id(id):
    SOLR_QUERY = 'select?q=id:'+id
    SOLR_QUERY_ARGS = '&fl=id,nombre,lider,email_lider, url_gruplac,proyectos,investigadores'
    req = SOLR_URL+SOLR_CORE_GRUPOS+SOLR_QUERY+SOLR_QUERY_ARGS
    response = r.get(req).json().get('response')
    return response

def get_researchers_results(query,num=10, inicio=0):
    SOLR_QUERY='select?defType=dismax&q='+query+' & qf=nombre + grupos + proyectos'
    SOLR_QUERY_ARGS = '&fl=id,nombre'
    SOLR_QUERY_PAG = '&rows='+str(num)+'&start='+str(inicio) 
    req = SOLR_URL+SOLR_CORE_INVESTIGADORES+SOLR_QUERY+SOLR_QUERY_ARGS+SOLR_QUERY_PAG
    response = r.get(req).json().get('response')
    return response

def get_researcher_by_id(id):
    SOLR_QUERY = 'select?q=id:'+id
    SOLR_QUERY_ARGS = '&fl=id,nombre,unidad_negocio,departamento,grupos,proyectos'
    req = SOLR_URL+SOLR_CORE_INVESTIGADORES+SOLR_QUERY+SOLR_QUERY_ARGS
    response = r.get(req).json().get('response')
    return response
