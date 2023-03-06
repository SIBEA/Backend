#Modulo responsable de automatizar la generacion de los vectores y su guardado en archivos .json
from nlp import embeddings
#from sentence_transformers import SentenceTransformer

#nombre de los modelos sobre los cuales se quieren generar vectores
models = [
        'model_minilm',
        'model_mpnet',
        'model_multilingual_distiluse_v1',
        'model_multilingual_distiluse_v2',
        'model_multilingual_minilm',
        'model_multilingual_mpnet']


def generate():
    for m in models:
        embeddings.embeddings2json(m)

generate()