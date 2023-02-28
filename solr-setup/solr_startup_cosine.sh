#Testings made using solr 9.1.1
#Core creation 

bin/solr create -c model_minilm

bin/solr create -c model_mpnet

bin/solr create -c model_multilingual_distiluse_v1

bin/solr create -c model_multilingual_distiluse_v2

bin/solr create -c model_multilingual_minilm

bin/solr create -c model_multilingual_mpnet

#Initializing schema fields

#model_minilm 384

curl http://localhost:8983/solr/model_minilm/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_384",
"indexed":true,
"stored":true
}
]
}'


#model_mpnet 768

curl http://localhost:8983/solr/model_mpnet/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_768",
"indexed":true,
"stored":true
}
]
}'


#model_multilingual_distiluse_v1 512

curl http://localhost:8983/solr/model_multilingual_distiluse_v1/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_512",
"indexed":true,
"stored":true
}
]
}'


#model_multilingual_distiluse_v2 512

curl http://localhost:8983/solr/model_multilingual_distiluse_v2/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_512",
"indexed":true,
"stored":true
}
]
}'

#model_multilingual_minilm 384

curl http://localhost:8983/solr/model_multilingual_minilm/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_384",
"indexed":true,
"stored":true
}
]
}'

#model_multilingual_mpnet 768

curl http://localhost:8983/solr/model_multilingual_mpnet/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"titulo",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"facultad",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"departamento",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
}, 
{
"name":"resumen",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"objetivos",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"palabras_clave",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},  
{    
"name":"vector",
"type":"knn_vector_768",
"indexed":true,
"stored":true
}
]
}'

## Indexing Documents
