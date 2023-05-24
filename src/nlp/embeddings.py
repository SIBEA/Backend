from sentence_transformers import SentenceTransformer
from nlp.dataframe_processing import get_dataframe
import json
import os


this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)

#model_path = 'models/embeddings'
"""##Carga el dataframe y enlaza en un diccionario el vector correspondiente
def append_embeddings(messages):   
    #print("generando embeddings para el modelo "+model)     
    results = []
    
    #df[["titulo_del_proyecto","nombre_facultad","nombre_del_departamento","descripcion","resumen","objetivos","metodologia","gran_area","objetivo_socioeconomico","palabras_clave"]]
    i = 0
    for index,row in messages.iterrows():
        embedString = messages.at[index,"corpus"]
       # print(embedString)
        embedding = embed(embedString)
        print("Documentos vectorizados: "+str(i))
        i=i+1
        results.append({"titulo":row["titulo_del_proyecto"],"facultad":row["nombre_facultad"],"departamento":row["nombre_del_departamento"],"resumen":row["resumen"],"objetivos":row["objetivos"],"palabras_clave":row["palabras_clave"],"vector":embedding.tolist()})
    return results
"""

##Vectorizado de uso general, TODO: Delegar el cargue del modelo al modulo "load model".
def embed(messages):
    #this_file = os.path.abspath(__file__)
    #this_dir = os.path.dirname(this_file)    
    #wanted_dir = os.path.join(this_dir,model_path)
    #model = SentenceTransformer(wanted_dir) 
    return SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2') .encode(messages, normalize_embeddings=True)

"""
def embeddings2json():
    #Generando el dataframe ()
    df = get_dataframe()    
    #Se crea un diccionario con ciertos datos del dataframe y se adjunta el vector correspondiente
    dict = append_embeddings(df,model)
    #print("generando archivo JSON para el modelo "+model)    
    j = json.dumps(dict)    
    jsonFile = open(os.path.join(this_dir,"./json/"+model+".json"), "w")
    jsonFile.write(j)
    jsonFile.close()
    print(json)
    return json
"""



