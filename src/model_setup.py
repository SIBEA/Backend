#Este modulo descarga los modelos a la ruta indicada
from sentence_transformers import SentenceTransformer


models = {
    'model_minilm':'all-MiniLM-L6-v2',
    'model_mpnet':'all-mpnet-base-v2',
    'model_multilingual_distiluse_v1':'distiluse-base-multilingual-cased-v1',
    'model_multilingual_distiluse_v2':'distiluse-base-multilingual-cased-v2',
    'model_multilingual_minilm':'paraphrase-multilingual-MiniLM-L12-v2',
    'model_multilingual_mpnet':'paraphrase-multilingual-mpnet-base-v2'}


path = './nlp/models'



for m in models:
    SentenceTransformer(models[m]).save(path+m)
    

