from sentence_transformers import SentenceTransformer
import pandas as pd
import json
from unidecode import unidecode
import numpy as np
import os

this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
path = 'models/model_multilingual_distiluse_v2'
wanted_dir = os.path.join(this_dir,path)

def get_dataframe_test():
    print("procesando datos...")
    
    inv_df = pd.read_excel(os.path.join(this_dir,'./xlsx/InvestigarPUJ.xlsx'), sheet_name='Hoja1', converters={'ID PROYECTO':str})
    siap_df = pd.read_excel(os.path.join(this_dir,'./xlsx/Descriptores SIAP 2023.xlsx'), sheet_name='SIAP ', converters={'ID Proy':str})
    inv_full_df = pd.read_excel(os.path.join(this_dir,'./xlsx/Descriptores SIAP 2023.xlsx'), sheet_name='InvestigarPUJ', converters={'Id':str})

    inv_full_df.drop("Año", axis=1, inplace=True)

    datasets = [inv_df, siap_df, inv_full_df]
    for dataset in datasets:
        dataset.replace('\\N', np.NaN, inplace=True)
        dataset.replace('null', np.NaN, inplace=True)
        dataset.replace('nan', np.NaN, inplace=True)
        dataset.replace('N/A', np.NaN, inplace=True)


    merged = inv_df.merge(siap_df, left_on="ID PROYECTO", right_on="ID Proy", how="left")
    df = merged.merge(inv_full_df, left_on="ID PROYECTO", right_on="Id", how="left")
    
    df = df.groupby("ID PROYECTO").agg(lambda x: list(set(x))).applymap(lambda x: ', '.join(str(y) for y in x if str(y) != 'nan') if isinstance(x, list) else x)
    df = df.reset_index()
    df.columns = [unidecode(x.lower().strip().replace(" ", "_").replace("__", "_").replace(".", "")) for x in df.columns]

    df.replace('', np.NaN, inplace=True)

    df["descripcion"] = df["descripcion_x"].fillna("") + df["descripcion_y"].fillna("")

    df.drop("titulo_x", axis=1, inplace=True)
    df.drop("titulo_y", axis=1, inplace=True)
    df.drop("id_proy", axis=1, inplace=True)
    df.drop("id", axis=1, inplace=True)
    df.drop("financiador", axis=1, inplace=True)
    df.drop("tipo_propuesta", axis=1, inplace=True)
    df.drop("descripcion_x", axis=1, inplace=True)
    df.drop("descripcion_y", axis=1, inplace=True)
    df.drop("id_propt", axis=1, inplace=True)
    df.drop("f_inic_real", axis=1, inplace=True)
    df.drop("f_final_real", axis=1, inplace=True)
    df.drop("facultad", axis=1, inplace=True)
    df.drop("departamento", axis=1, inplace=True)
    df.drop("estado_proyecto", axis=1, inplace=True)
    df.drop("nombre", axis=1, inplace=True)
    df.drop("cantidad", axis=1, inplace=True)
    df.drop("fecha_de_negociacion", axis=1, inplace=True)
    df.drop("fecha_inicial_real", axis=1, inplace=True)
    df.drop("fecha_final_real", axis=1, inplace=True)
    df.drop("convocatoria", axis=1, inplace=True)
    df.drop("miembro_del_equipo", axis=1, inplace=True)
    #print(df.columns)
    #print(df.shape)

    #df[df["id_proyecto"] == "000000000007161"]
    #df[df["id_proyecto"] == "004438"]
    #df[df["id_proyecto"] == "20104"]
    df["corpus"] = df["titulo_del_proyecto"].fillna("") + " "  + \
    df["nombre_facultad"].str.split().str[-1].fillna("") + " " + \
    df["nombre_del_departamento"].str.split().str[-1].fillna("") + " "
    newdf = df[["corpus","titulo_del_proyecto","nombre_facultad","nombre_del_departamento","descripcion","resumen","objetivos","metodologia","gran_area","objetivo_socioeconomico","palabras_clave"]]
    df.to_csv("./merged.csv", index=False)


    #df["corpus"] = df["corpus"].replace(r'\n',' ', regex=True).str.strip()

    #newdf.to_csv("./csv/test.csv", index=False)
    return df


def append_embeddings(messages,model):   
    print("generando embeddings para el modelo "+model)     
    results = []
    
    #df[["titulo_del_proyecto","nombre_facultad","nombre_del_departamento","descripcion","resumen","objetivos","metodologia","gran_area","objetivo_socioeconomico","palabras_clave"]]
    i = 0
    for index,row in messages.iterrows():
        embedString = messages.at[index,"corpus"]
       # print(embedString)
       # embedding = embed(embedString,model)
        print("Documentos vectorizados: "+embedString)
        i=i+1
        #results.append({"titulo":row["titulo_del_proyecto"],"facultad":row["nombre_facultad"],"departamento":row["nombre_del_departamento"],"resumen":row["resumen"],"objetivos":row["objetivos"],"palabras_clave":row["palabras_clave"],"vector":embedding.tolist()})
    return results


df = get_dataframe_test()

append_embeddings(df,'asd')