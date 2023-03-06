#Core deletion, just in case

bin/solr delete -c model_minilm_cosine

bin/solr delete -c model_mpnet_cosine

bin/solr delete -c model_multilingual_distiluse_v1_cosine

bin/solr delete -c model_multilingual_distiluse_v2_cosine

bin/solr delete -c model_multilingual_minilm_cosine

bin/solr delete -c model_multilingual_mpnet_cosine

#Testings made using solr 9.1.1
#Core creation

bin/solr create -c model_minilm_cosine

bin/solr create -c model_mpnet_cosine 

bin/solr create -c model_multilingual_distiluse_v1_cosine

bin/solr create -c model_multilingual_distiluse_v2_cosine

bin/solr create -c model_multilingual_minilm_cosine

bin/solr create -c model_multilingual_mpnet_cosine

#Initializing schema fields

#model_minilm 384

curl http://localhost:8983/solr/model_minilm_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

curl http://localhost:8983/solr/model_mpnet_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

curl http://localhost:8983/solr/model_multilingual_distiluse_v1_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

curl http://localhost:8983/solr/model_multilingual_distiluse_v2_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

curl http://localhost:8983/solr/model_multilingual_minilm_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

curl http://localhost:8983/solr/model_multilingual_mpnet_cosine/schema -X POST -H 'Content-type:application/json' --data-binary '{
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

bin/post -c model_minilm_cosine /home/embeddings/model_minilm.json

bin/post -c model_mpnet_cosine /home/embeddings/model_mpnet.json

bin/post -c model_multilingual_distiluse_v1_cosine /home/embeddings/model_multilingual_distiluse_v1.json

bin/post -c model_multilingual_distiluse_v2_cosine /home/embeddings/model_multilingual_distiluse_v2.json

bin/post -c model_multilingual_minilm_cosine /home/embeddings/model_multilingual_minilm.json

bin/post -c model_multilingual_mpnet_cosine /home/embeddings/model_multilingual_mpnet.json