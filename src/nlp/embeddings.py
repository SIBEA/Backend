from sentence_transformers import SentenceTransformer
from nlp.dataframe_processing import get_dataframe
import json
import os


this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)


##Carga el dataframe y enlaza en un diccionario el vector correspondiente
def append_embeddings(messages,model):   
    print("generando embeddings para el modelo "+model)     
    results = []
    
    #df[["titulo_del_proyecto","nombre_facultad","nombre_del_departamento","descripcion","resumen","objetivos","metodologia","gran_area","objetivo_socioeconomico","palabras_clave"]]
    i = 0
    for index,row in messages.iterrows():
        embedString = messages.at[index,"corpus"]
       # print(embedString)
        embedding = embed(embedString,model)
        print("Documentos vectorizados: "+str(i))
        i=i+1
        results.append({"titulo":row["titulo_del_proyecto"],"facultad":row["nombre_facultad"],"departamento":row["nombre_del_departamento"],"resumen":row["resumen"],"objetivos":row["objetivos"],"palabras_clave":row["palabras_clave"],"vector":embedding.tolist()})
    return results

'model_minilm'
'model_mpnet'
'model_multilingual_distiluse_v1'
'model_multilingual_distiluse_v2'
'model_multilingual_minilm'
'model_multilingual_mpnet'

##Vectorizado de uso general, TODO: Delegar el cargue del modelo al modulo "load model".
def embed(messages,model):
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    if model=='model_minilm':
        path = 'models/model_minilm'
        wanted_dir = os.path.join(this_dir,path)
    elif model == 'model_mpnet':
        path = 'models/model_mpnet'
        wanted_dir = os.path.join(this_dir,path)
    elif model == 'model_multilingual_distiluse_v1':
        path = 'models/model_multilingual_distiluse_v1'
        wanted_dir = os.path.join(this_dir,path)
    elif model == 'model_multilingual_distiluse_v2':
        path = 'models/model_multilingual_distiluse_v2'
        wanted_dir = os.path.join(this_dir,path)
    elif model == 'model_multilingual_minilm':
        path = 'models/model_multilingual_minilm'
        wanted_dir = os.path.join(this_dir,path)
    elif model == 'model_multilingual_mpnet':
        path = 'models/model_multilingual_mpnet'
        wanted_dir = os.path.join(this_dir,path)
    model = SentenceTransformer(wanted_dir) 
    return model.encode(messages, normalize_embeddings=True)


def embeddings2json(model):
    #Generando el dataframe ()
    df = get_dataframe()    
    #Se crea un diccionario con ciertos datos del dataframe y se adjunta el vector correspondiente
    dict = append_embeddings(df,model)
    print("generando archivo JSON para el modelo "+model)    
    j = json.dumps(dict)    
    jsonFile = open(os.path.join(this_dir,"./json/"+model+".json"), "w")
    jsonFile.write(j)
    jsonFile.close()
    print(json)
    return json




