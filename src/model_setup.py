from sentence_transformers import SentenceTransformer


models = ['paraphrase-multilingual-mpnet-base-v2']


path = './nlp/models/'



for m in models:
    SentenceTransformer(m).save(path+'/embeddings')
    

