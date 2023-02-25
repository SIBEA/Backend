"""
1 - Load a model from disk
2 - If the model is not on disk, download it first
"""

#TODO: Delegar el cargue de modelos a este modulo
from sentence_transformers import SentenceTransformer

class ModelLoader:
    def get_model_multilingual_distiluse_v2():        
        path = './models/model_multilingual_distiluse_v2'
        model = SentenceTransformer(path)
        return model