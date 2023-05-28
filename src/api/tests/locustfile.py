from locust import HttpUser, task, between
import random

queries = ['paz','guerra','pacientes','lgbt','Investigacion','Camilo','Proyecto','Colombia,',
           'Diseño y construcción de una plataforma robótica de exploración y reparación de tuberías hidrosanitarias, operada remotamente.',
           'Significación del discurso teológico hoy',
           'Academia',
           'Aprendizaje y sociedad de la información']

FILTRO_PROP = ['\"Proyecto de investigación: Investigación\"',
 '\"Actividad de investigación: Apoyo a nuevas publicaciones\"',
 '\"Proyecto de innovación: Spin-Off\"',
 '\"Actividad de investigación: Movilidad-Internacional\"',
 '\"Actividad de investigación: Otros apoyos\"',
 '\"Proyecto de innovación: Prueba concepto\"',
 '\"Proyecto de innovación: Universidad empresa\"',
 '\"Proyecto de innovación: Innovación\"']

FILTRO_ESTADO = ['\"Terminado\"', '\"Pendiente Compromiso\"', '\"En Liquidación\"', '\"En Ejecución\"'] 

FILTRO_COMUNIDADES = ['sin_filtrar','con_comunidades','sin_comunidades']

class User(HttpUser):
    wait_time=between(0,1)


    #Task for testing load on search general
    @task
    def search_projects_nofilters(self):
        query = random.choice(queries)
        num = random.randint(100,500)
        inicio = 0
        self.client.get('search/proyectos/'+str(query)+'?num='+str(num)+'&inicio='+str(inicio)+'&comunidades=sin_filtrar')

    #Task for testing load on search general with filters
    @task
    def search_projects_filters(self):
        query = random.choice(queries)
        num = random.randint(100,500)
        propuesta = random.choice(FILTRO_PROP)
        estado = random.choice(FILTRO_ESTADO)
        comunidad = random.choice(FILTRO_COMUNIDADES)
        inicio = 0
        self.client.get('search/proyectos/'+str(query)+'?num='+str(num)+'&inicio='+str(inicio)+'&propuesta='+propuesta+'&estado='+estado+'&comunidades='+comunidad)

        #http://localhost:8000/search/proyectos/{titulo}/topk?query=asdas&num=10&inicio=0

    #Task for testing load on top k  component
    @task
    def search_projects_topk(self):
        query = random.choice(queries)
        num = random.randint(100,500)
        inicio = 0
        self.client.get('search/proyectos/topk/'+str(query))
    
    #Task for testing load on top k title component
    @task
    def search_projects_topk_title(self):
        query = random.choice(queries)
        num = random.randint(100,500)
        inicio = 0
        self.client.get('search/proyectos/'+str(query)+'/topk?query='+query)

    #Task for testing load on communities
    @task
    def search_projects_communities(self):
        query = random.choice(queries)
        self.client.get('search/proyectos/communities/'+str(query))

    #Task for testing load on coordinates
    @task
    def search_projects_coordinates(self):
        query = random.choice(queries)
        self.client.get('search/proyectos/coordinates/'+str(query))

    #Task for testing load on coordinates
    @task
    def search_grupos(self):
        query = random.choice(queries)
        self.client.get('search/grupos/'+str(query))
        
    #Task for testing load on coordinates
    @task
    def search_investigadores(self):
        query = random.choice(queries)
        self.client.get('search/investigadores/'+str(query))

    

