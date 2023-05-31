import spacy
import os

class NER_Model:
    def __init__(self,path):
        print(path)
        self.nlp = spacy.load(path)

    def get_entity(self,text):
        ents = []
        doc = self.nlp(text)
        for ent in doc.ents:
            ents.append(ent.text)
        return ents
    
