#Testings made using solr 9.1.1
#Core creation

bin/solr create -c model_minilm_dot

bin/solr create -c model_mpnet_dot 

bin/solr create -c model_multilingual_distiluse_v1_dot

bin/solr create -c model_multilingual_distiluse_v2_dot

bin/solr create -c model_multilingual_minilm_dot

bin/solr create -c model_multilingual_mpnet_dot

#Initializing schema fields

#model_minilm 384

curl http://localhost:8983/solr/model_minilm_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"dot_product",
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

curl http://localhost:8983/solr/model_mpnet_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"dot_product",
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

curl http://localhost:8983/solr/model_multilingual_distiluse_v1_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"dot_product",
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

curl http://localhost:8983/solr/model_multilingual_distiluse_v2_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"dot_product",
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

curl http://localhost:8983/solr/model_multilingual_minilm_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"dot_product",
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

curl http://localhost:8983/solr/model_multilingual_mpnet_dot/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"dot_product",
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

bin/post -c model_minilm_dot /home/embeddings/model_minilm.json

bin/post -c model_mpnet_dot /home/embeddings/model_mpnet.json

bin/post -c model_multilingual_distiluse_v1_dot /home/embeddings/model_multilingual_distiluse_v1.json

bin/post -c model_multilingual_distiluse_v2_dot /home/embeddings/model_multilingual_distiluse_v2.json

bin/post -c model_multilingual_minilm_dot /home/embeddings/model_multilingual_minilm.json

bin/post -c model_multilingual_mpnet_dot /home/embeddings/model_multilingual_mpnet.json