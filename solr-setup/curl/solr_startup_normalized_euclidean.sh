curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_minilm_euclidean&configSet=model_minilm_euclidean'
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_mpnet_euclidean&configSet=model_mpnet_euclidean'
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_multilingual_distiluse_v1_euclidean&configSet=model_multilingual_distiluse_v1_euclidean'
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_multilingual_distiluse_v2_euclidean&configSet=model_multilingual_distiluse_v2_euclidean'
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_multilingual_minilm_euclidean&configSet=model_multilingual_minilm_euclidean'
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=model_multilingual_mpnet_euclidean&configSet=model_multilingual_mpnet_euclidean'

#model_minilm 384

curl http://solr:8983/solr/model_minilm_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"euclidean",
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

curl http://solr:8983/solr/model_mpnet_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"euclidean",
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

curl http://solr:8983/solr/model_multilingual_distiluse_v1_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"euclidean",
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

curl http://solr:8983/solr/model_multilingual_distiluse_v2_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_512",
"class":"solr.DenseVectorField",
"vectorDimension":512,
"similarityFunction":"euclidean",
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

curl http://solr:8983/solr/model_multilingual_minilm_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_384",
"class":"solr.DenseVectorField",
"vectorDimension":384,
"similarityFunction":"euclidean",
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

curl http://solr:8983/solr/model_multilingual_mpnet_euclidean/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"euclidean",
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


curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_minilm_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_minilm.json
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_mpnet_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_mpnet.json
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_multilingual_distiluse_v1_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_multilingual_distiluse_v1.json
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_multilingual_distiluse_v2_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_multilingual_distiluse_v2.json
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_multilingual_minilm_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_multilingual_minilm.json
curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/model_multilingual_mpnet_euclidean/update?commit=true&wt=json' -d @/home/embeddings/model_multilingual_mpnet.json