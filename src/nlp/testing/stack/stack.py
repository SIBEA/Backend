import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from sentence_transformers import SentenceTransformer, util
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
from simpleneighbors import SimpleNeighbors
from tqdm import tqdm
from tqdm import trange
import tensorflow.compat.v2 as tf
import torch
import time
from unidecode import unidecode
import math
import faiss


def generate_corpus_embeddings(messages, model):
    print("Generating corpus embeddings...")
    if (os.path.exists('./index_embeddings')):
        print("Loading index...")
        return torch.load('./index_embeddings')

    start_encoding = time.time()
    embeddings_multilingual_minilm = model.encode(messages)
    end_encoding = time.time()
    torch.save(embeddings_multilingual_minilm, './index_embeddings')
    print("Encoding time: ", end_encoding - start_encoding)
    return embeddings_multilingual_minilm


def search(query, corpus_embeddings, top_k=10, model=None):
    print("Searching...")
    query_embeddings = model.encode([query])
    hits = util.semantic_search(
        query_embeddings, corpus_embeddings, top_k=top_k)
    return np.array([hit['corpus_id'] for hit in hits[0]])

def get_results(results, df):
    print("Getting results...")
    labels = []
    titles = [df.iloc[[i]]["titulo_del_proyecto"].values[0] for i in results]
    for title_index, title in enumerate(titles):
        labels.append((str(title_index + 1) + ". " + title))

    return pd.DataFrame.from_dict(labels)

def generate_corups():
    print("Generating corpus...")
    inv_df = pd.read_excel('./xlsx/InvestigarPUJ.xlsx',
                           sheet_name='Hoja1', converters={'ID PROYECTO': str})
    siap_df = pd.read_excel('./xlsx/Descriptores SIAP 2023.xlsx',
                            sheet_name='SIAP ', converters={'ID Proy': str})
    inv_full_df = pd.read_excel(
        './xlsx/Descriptores SIAP 2023.xlsx', sheet_name='InvestigarPUJ', converters={'Id': str})

    inv_full_df.drop("Año", axis=1, inplace=True)

    datasets = [inv_df, siap_df, inv_full_df]
    for dataset in datasets:
        dataset.replace('\\N', np.NaN, inplace=True)
        dataset.replace('null', np.NaN, inplace=True)
        dataset.replace('nan', np.NaN, inplace=True)
        dataset.replace('N/A', np.NaN, inplace=True)

    merged = inv_df.merge(siap_df, left_on="ID PROYECTO",
                          right_on="ID Proy", how="left")
    df = merged.merge(inv_full_df, left_on="ID PROYECTO",
                      right_on="Id", how="left")

    df = df.groupby("ID PROYECTO").agg(lambda x: list(set(x))).applymap(
        lambda x: ', '.join(str(y) for y in x if str(y) != 'nan') if isinstance(x, list) else x)
    df = df.reset_index()
    df.columns = [unidecode(x.lower().strip().replace(" ", "_").replace(
        "__", "_").replace(".", "")) for x in df.columns]

    df.replace('', np.NaN, inplace=True)

    df["descripcion"] = df["descripcion_x"].fillna(
        "") + df["descripcion_y"].fillna("")

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

    df = df[(df["tipo_de_propuesta"] == "ART") |
            (df["tipo_de_propuesta"] == "INN") |
            (df["tipo_de_propuesta"] == "NEW") |
            (df["tipo_de_propuesta"] == "PCA") |
            (df["tipo_de_propuesta"] == "PIS") |
            (df["tipo_de_propuesta"] == "PPC") |
            (df["tipo_de_propuesta"] == "PUE")]

    df["corpus"] = df["titulo_del_proyecto"].fillna("") + " " + \
        df["nombre_facultad"].str.split().str[-1].fillna("") + " " + \
        df["nombre_del_departamento"].str.split().str[-1].fillna("") + " " + \
        df["descripcion"].fillna("") + " " + \
        df["resumen"].fillna("") + " " + \
        df["objetivos"].fillna("") + " " + \
        df["metodologia"].fillna("") + " " + \
        df["gran_area"].fillna("") + " " + \
        df["objetivo_socioeconomico"].fillna("") + " " + \
        df["palabras_clave"].fillna("")

    df["corpus"] = df["corpus"].replace(r'\n', ' ', regex=True).str.strip()

    print(df.shape)

    return (df["corpus"].to_numpy(), df)


if __name__ == "__main__":
    model = SentenceTransformer(
        'paraphrase-multilingual-MiniLM-L12-v2')
    (messages, df) = generate_corups()
    embeddings = generate_corpus_embeddings(messages, model)
    search_results = search("Guerra", embeddings, 10, model)
    results = get_results(search_results, df).to_numpy()
    print(results)
