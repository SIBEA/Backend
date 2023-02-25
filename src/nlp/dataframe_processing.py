import pandas as pd
import numpy as np
from unidecode import unidecode
import os
##Load and perform transformations on a pandas DF
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)

##columnas a descartar luego de unificar los dataframes
list_columns_drop = ['ano',
                     'nombre_patrocinador',
                     'tipo_de_documento',
                     'numero_de_documento',
                     'nombres_y_apellidos',
                     'rol_en_el_proyecto',
                     'porcentaje_dedicacion',
                     'codigo_presupuesto',
                     'codigo_contrato_secre_juridica',
                     'valor_aprobado_patrocinador',
                     'contrapartida_terceros',
                     'contrapartida_rec_propi',
                     'contrapartida_rec_nuevo',
                     'rec_nuevos_unidade_academica',
                     'valor_contrapartida_total',
                     'valor_total',
                     'fecha_estimada_inicio',
                     'fecha_estimada_fin',
                     'id_empleado_responsable_puj',
                     'nombre_responsable_puj',
                     'departamento_responsable_puj',
                     'id_departamento_responsable_puj',
                     'facultad_responsable_puj',
                     'producto',
                     'valor_solicitado_a_financiador_principal',
                     'valor_total_financiadores',
                     'tipo_de_investigacion'            
]



def get_dataframe():
    print("procesando datos...")
    #Cargue de data
    inv_df = pd.read_excel(os.path.join(this_dir,'./xlsx/InvestigarPUJ.xlsx'), sheet_name='Hoja1', converters={'ID PROYECTO':str})
    siap_df = pd.read_excel(os.path.join(this_dir,'./xlsx/Descriptores SIAP 2023.xlsx'), sheet_name='SIAP ', converters={'ID Proy':str})
    inv_full_df = pd.read_excel(os.path.join(this_dir,'./xlsx/Descriptores SIAP 2023.xlsx'), sheet_name='InvestigarPUJ', converters={'Id':str})

    inv_full_df.drop("Año", axis=1, inplace=True)

    #primera tanda de limpieza, remover nulos y datos basura
    datasets = [inv_df, siap_df, inv_full_df]
    for dataset in datasets:
        dataset.replace('\\N', np.NaN, inplace=True)
        dataset.replace('null', np.NaN, inplace=True)
        dataset.replace('nan', np.NaN, inplace=True)
        dataset.replace('N/A', np.NaN, inplace=True)

    #unir los dataframes
    merged = inv_df.merge(siap_df, left_on="ID PROYECTO", right_on="ID Proy", how="left")
    df = merged.merge(inv_full_df, left_on="ID PROYECTO", right_on="Id", how="left")

    df = df.groupby("ID PROYECTO").agg(lambda x: list(set(x))).applymap(lambda x: ', '.join(str(y) for y in x if str(y) != 'nan') if isinstance(x, list) else x)
    df = df.reset_index()
    df.columns = [unidecode(x.lower().strip().replace(" ", "_").replace("__", "_").replace(".", "")) for x in df.columns]

    df.replace('', np.NaN, inplace=True)
    #segunda tanda de limpieza, eliminacion de columnas no relevantes
    df["descripcion"] = df["descripcion_x"].fillna("") + df["descripcion_y"].fillna("")
    
    #TODO: Mover estos valores a la lista de columnas a dropear
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

    df.drop(list_columns_drop,axis = 1, inplace=True)

    #Creacion del corpus
    df["corpus"] = df["titulo_del_proyecto"].fillna("") + " "  + \
    df["nombre_facultad"].str.split().str[-1].fillna("") + " " + \
    df["nombre_del_departamento"].str.split().str[-1].fillna("") + " " + \
    df["descripcion"].fillna("") + " " + \
    df["resumen"].fillna("") + " " + \
    df["objetivos"].fillna("") + " " + \
    df["metodologia"].fillna("") + " " + \
    df["gran_area"].fillna("") + " " + \
    df["objetivo_socioeconomico"].fillna("") + " " + \
    df["palabras_clave"].fillna("")

    #Tercera tanda de limpieza, remover filas que tengan como tipo de propuesta AJI
    df = df[df['tipo_de_propuesta']!='AJI']
    print(df[df['tipo_de_propuesta']=='AJI'])

    #Cuarta tanda de limpieza, eliminar tildes y acentuaciones del corpus

    for row,index in df.iterrows():
        df.at[row,"corpus"] = unidecode(df.at[row,"corpus"])


    return df

