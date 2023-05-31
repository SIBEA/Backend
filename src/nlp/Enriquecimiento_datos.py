import pandas as pd
import numpy as np
from unidecode import unidecode
from sentence_transformers import SentenceTransformer
from nlp.Embeddings_model import Transformer
from nlp.Spacy_pypeline import NER_Model
from geopy.geocoders import GoogleV3
import time
import json


ROL_INVESTIGADOR= {
    'ASES':'Asesor de Proyecto de investigacion',
    'ASIS':'Asistente de Proyecto de investigacion',
    'AUTO':'Autor Publicaciones',
    'COIN':'Co-Investigador de Proyecto de investigacion',
    'CPI':'Co-Investigador principal',
    'DOCT':'Doctorando',
    'EST':'Estudiante',
    'ESTU':'Estudiante',
    'JOIN':'Jóven Investigador',
    'OTH':'Otro',
    'PI':'Investigador Principal.',
    'POSD':'PostDoctor',
    'POSTDOCTOR':'PostDoctor',
    'TUT':'Tutor Joven Investigador'
}

TIPO_PROPUESTA = {
    'AJI':'Actividad de investigación: Apoyo a Jóvenes Investigadores',
    'ANP':'Actividad de investigación: Apoyo a nuevas publicaciones',
    'ART':'Proyecto de creación artística: Creación artística',
    'INN':'Proyecto de innovación: Innovación',
    'INT':'Actividad de investigación: Movilidad-Internacional',
    'NEW':'Proyecto de investigación: Investigación',
    'OAP':'Actividad de investigación: Otros apoyos',
    'PCA':'Proyecto de creación artística: Creación artística',
    'PIS':'Proyecto de innovación: Spin-Off',
    'PPC':'Proyecto de innovación: Prueba concepto',
    'PRD':'Proyecto recoleccion docencia',
    'PUE':'Proyecto de innovación: Universidad empresa',
    'SI':'Actividad de investigación: Semillero de Investigación'
}

characters_remove = "!\"#$%&'()*+-/:;<=>?@[\]^_`{|}~¿"
domain = "maps.googleapis.com"
API_KEY = ''


path_BETO = ''
path_TOK2VEC  = ''
path_DATALIMPIA = ''
path_HISTORICO_GRUPOS = ''
path_HISTORICO_INVESTIGADORES = ''
path_INVESTIGADORES = ''
path_GRUPOS = ''
path_DIVIPOLA = ''

model_embeddings = Transformer()
model_BETO = NER_Model(path_BETO)
model_TOK2VEC = NER_Model(path_TOK2VEC)
model_UBICACIONES = NER_Model('es_core_news_lg')

df_proyectos = df_proyectos =  pd.read_excel(path_DATALIMPIA)
df_investigadores = pd.read_excel(path_INVESTIGADORES)
df_grupos = pd.read_excel(path_GRUPOS)

df_grupos_historico = pd.read_excel(path_HISTORICO_GRUPOS)

#Utilidad para limpiar datos de la descripcion extendida
def clean_data(text, lowercase=False):
    if lowercase==True:
        print("lowercasing")
        text = text.lower()
    #text = unidecode(text)
    text = text.translate(str.maketrans(' ', ' ', characters_remove))
    #text = ''.join([i for i in text if not i.isdigit()])    
    text = text.replace('\n', ' ').replace('\r', '')
    #print(text)
    return text

"""
Retorna las predicciones del modelo BETO
"""
def get_keywords(desc_extendida):
    coms =  model_BETO.get_entity(desc_extendida)
    return coms

"""
Retorna las predicciones del modelo TOK2VEC
"""
def refine_tok2vec(coms_beto):
    coms = []
    for com in coms_beto:
        coms.append(model_TOK2VEC.get_entity(com))
    return com

"""
Retorna la informacion extendida de un grupo de informacion, se usa para complementar la informacion final.
"""
def get_grupos(grupos):
    list_grupo = []
    if isinstance(grupos,str):
        grupos = grupos.split('||')
        for g in grupos:
            if isinstance(g,str):
                df = df_grupos.loc[df_grupos['Grupo'] == g]
                if(df.empty == False):
                    #print(p)
                    id = str(df['ID'].values[0])
                    nombre = str(df['Grupo'].values[0])
                    list_grupo.append(id+';'+nombre)
    else:
        list_grupo.append('No asociado a grupos')
    return list_grupo


"""
Retorna la informacion extendida de un investigador, se usa para complementar la informacion final.
"""
def get_investigadores_relacionados(investigador):
    investigador = investigador.split('||')
    list_inv = []
    for i in investigador:
        if isinstance(i,str):
            df = df_investigadores.loc[df_investigadores['NOMBRES Y APELLIDOS'] == i]
            id = str(df['ID'].values[0])
            nombre = str(df['NOMBRES Y APELLIDOS'].values[0])
            list_inv.append(id+';'+nombre)
    return list_inv


"""
Retorna las predicciones de ubicaciones del modelo es_news_core_lg de spacy.
"""
def get_locations(desc_extendida):
    locations =  model_UBICACIONES.get_entity(desc_extendida)
    return locations


"""
Funcion Auxiliar que realiza el emparejamiento con DIVIPOLA en caso de que google geocode no arroje coordenadas.
"""
def use_divipola(l):
    df_divipola = pd.read_excel(path_DIVIPOLA)
    if df_divipola.loc[df_divipola['nombre_departamento'] == l].head(1).empty == False:
        df = df_divipola.loc[df_divipola['nombre_departamento'] == l].head(1)
        depto = df['nombre_departamento'].values[0]
        municipio = df['nombre_municipio'].values[0]
        poblado = df['nombre_municipio'].values[0]
        nombre = depto+' '+municipio+' '+poblado
        lat = df['latitud'].values[0]
        lon = df['longitud'].values[0]
        print(f'{nombre} {lat} {lon}')   
        return  str(nombre)+';'+str(lat)+';'+str(lon)+'+++'


"""
Retorna las coordenadas entregadas por google geocode.
"""
def geocode_list(list_location):
    geolocator = GoogleV3(api_key=API_KEY, domain = domain)
    coordinates = ''
    for l in list_location:
        if l:                        
            location = geolocator.geocode(l)   
            #Si google arroja resultado         
            if location:                
                coordinates+='+++'
                title = location.address
                lat = location.latitude
                lon = location.longitude                       
                coordinates+=str(title)+';'+str(lat)+';'+str(lon)+'+++'
                time.sleep(3)
            #Si google no arroja reultado, use Divipola
            else:
                coordinates = use_divipola(l)
    return coordinates

"""
Funcion Auxiliar que guarda un archivo JSON con codificacion UTF sin forzar el uso de ascii.
"""
def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4,ensure_ascii=False)

"""
Genera un diccionario con la informacion enriquecida de los proyectos.
"""
def generate_projects_list(df):
    list_projects = []
    i = 0
    for index,row in df.iterrows():
        id = row['ID']
        title = row['Título']
        propuesta = TIPO_PROPUESTA.get(row['TIPO DE PROPUESTA'])
        estado = row['Estado proyecto']
        fecha_inicio = row['FECHA INICIAL REAL']
        fecha_fin = row['FECHA FINAL REAL']        
        grupos = get_grupos(row['NOMBRE GRUPO DE INVESTIGACION'])
        descripcion = str(row['DESCR'])
        obj_general = str(row['OBJGE'])
        obj_especifico = str(row['OBJES'])
        metodologia = str(row['METODOLOG'])
        pertinencia = str(row['PERTI'])
        corpus = clean_data(row['corpus'])
        vector = model_embeddings.embed(corpus)
        sujeto_investigacion = get_keywords(corpus)
        comunidades = refine_tok2vec(sujeto_investigacion)        
        ubicaciones_ner = get_locations(corpus)
        ubicaciones = geocode_list(ubicaciones_ner)
        miembros = get_investigadores_relacionados(row['NOMBRES Y APELLIDOS'])                
        list_projects.append({
                              'id':id,'titulo':title,'propuesta':propuesta,'estado':estado,'fecha_inicio':fecha_inicio,'fecha_fin':fecha_fin,
                              'grupo':grupos,'miembros':miembros,'descripcion':descripcion,'obj_general':obj_general,
                              'obj_especifico':obj_especifico,'metodologia':metodologia,'pertinencia':pertinencia,
                              'vector':vector,'comunidades':comunidades,'sujeto_investigacion':sujeto_investigacion,'ubicaciones':ubicaciones                              
                            })
        i+=1
        print(f'quedan {len(df)-i} proyectos')
    return list_projects  


"""
Funcion auxiliar para enriquecer la informacion de los grupos.
"""
def get_info_historico(grupo):
    df = df_grupos_historico.loc[df_grupos_historico['Grupo'] == grupo.lower()]
    if(df.empty == False):
        lider = str(df['Líder'].values[0])
        email_lider = str(df['Email'].values[0])
        url_gruplac = str(df['URL'].values[0])
        return {'lider':lider,'email_lider':email_lider,'url_gruplac':url_gruplac}
    else:
        return {'lider':'nan','email_lider':'nan','url_gruplac':'nan'}

"""
Funcion auxiliar obtener los proyectos con los que ha trabajado un grupo o investigador.
"""
def get_proyectos(proyectos):
    proyectos = proyectos.split('||')
    list_proy = []
    for p in proyectos:
        if isinstance(p,str):
            df = df_proyectos.loc[df_proyectos['Título'] == p]
            if(df.empty == False):
                #print(p)
                id = str(df['ID'].values[0])
                titulo = clean_data(str(df['Título'].values[0]))
                list_proy.append(id+';'+titulo)
    return list_proy

"""
Genera un diccionario con la informacion de los grupos.
"""
def generate_group_list(df):
    list_groups = []
    i = 0
    for index,row in df.iterrows():
        id = row['ID']
        nombre = row['Grupo']
        historico = get_info_historico(nombre)
        lider = historico.get('lider')
        email_lider = historico.get('email_lider')
        url_gruplac = historico.get('url_gruplac')
        investigadores = get_investigadores_relacionados(row['NOMBRES Y APELLIDOS'])
        proyectos = get_proyectos(row['Título'])
        list_groups.append({'id':id,'nombre':nombre,'lider':lider,'email_lider':email_lider,'url_gruplac':url_gruplac,'investigadores':investigadores,'proyectos':proyectos})
        i+=1
        print(f'quedan {len(df)-i} grupos')
    return list_groups   


"""
Genera un diccionario con la informacion de los investigadores.
"""
def generate_researcher_list(df):
    list_researcher = []
    i = 0
    for index,row in df.iterrows():
        id = row['ID']
        nombre = row['NOMBRES Y APELLIDOS']
        historico = get_info_historico(nombre)
        unidad_negocio = historico.get('unidad_negocio')
        departamento = historico.get('departamento')        
        grupos = get_grupos(row['Grupo'])
        proyectos = get_proyectos(row['Título'])
        list_researcher.append({'id':id,'nombre':nombre,'unidad_negocio':unidad_negocio,'departamento':departamento,'grupos':grupos,'proyectos':proyectos,})
        i+=1
        print(f'quedan {len(df)-i} investigadores')
    return list_researcher     


"""
guarda los datos de proyectos en un archivo json.
"""
def save_data_projects(route_file):
    list_projects = generate_projects_list(df_proyectos)
    write_data(route_file, list_projects)

"""
guarda los datos de grupos en un archivo json.
"""
def save_data_groups(route_file):
    list_groups = generate_projects_list(df_proyectos)
    write_data(route_file, list_groups)


"""
guarda los datos de investigadores en un archivo json.
"""
def save_data_researchers(route_file):
    list_researchers = generate_projects_list(df_proyectos)
    write_data(route_file, list_researchers)

"""
funcion principal, enriquece los proyectos, obtiene los datos de grupos e investigadores y genera archivos JSON listos para ser indexados a Solr.
"""
def enriquecer_informacion():
    path_out_projectos = ''
    path_out_grupos = ''
    path_out_investigadores = ''
    save_data_projects(path_out_projectos)
    save_data_groups(path_out_grupos)
    save_data_researchers(path_out_investigadores)



