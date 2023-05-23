from sentence_transformers import SentenceTransformer
import os

class Transformer:
    def __init__(self,path=os.path.dirname(os.getcwd())+'/models/embeddings'):
        self.model = SentenceTransformer(path)

    def embed(self,text):
        return self.model.encode(text, normalize_embeddings=True)




