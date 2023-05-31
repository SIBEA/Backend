curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=proyectos&configSet=proyectos'


curl http://solr:8983/solr/proyectos/schema -X POST -H 'Content-Type: application/json' --data-binary '{
  "add-field-type" : {
    "name":"text_custom",
    "class":"solr.TextField",
    "omitNorms":"false",
    "analyzer" : {
      "type" : "index",
      "tokenizer" : {
        "class":"solr.WhitespaceTokenizerFactory"
      },
      "filters" : [
        {
          "class":"solr.LowerCaseFilterFactory"
        },
        {
          "class":"solr.ASCIIFoldingFilterFactory",
          "preserveOriginal":true
        },
        {
          "class":"solr.EdgeNGramFilterFactory",
          "minGramSize":"4",
          "maxGramSize":"4",
          "preserveOriginal":"true"
        }
      ]
    },
    "analyzer" : {
      "type" : "query",
      "tokenizer" : {
        "class":"solr.WhitespaceTokenizerFactory"
      },
      "filters" : [
        {
          "class":"solr.LowerCaseFilterFactory"
        },
        {
          "class":"solr.ASCIIFoldingFilterFactory",
          "preserveOriginal":true
        },
        {
          "class":"solr.EdgeNGramFilterFactory",
          "minGramSize":"4",
          "maxGramSize":"4",
          "preserveOriginal":"true"
        }
      ]
    }
  }
}' 


curl http://solr:8983/solr/proyectos/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field-type" : {
"name":"knn_vector_768",
"class":"solr.DenseVectorField",
"vectorDimension":768,
"similarityFunction":"cosine",
"knnAlgorithm":"hnsw"
},
"add-field" : [
{
"name":"title",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"grupo",
"type":"text_custom",
"multiValued":false,
"stored":true,
"multiValued":true
},  
{
"name":"descripcion",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"obj_general",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"obj_especifico",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"metodologia",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"pertinencia",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"propuesta",
"type":"string",
"multiValued":false,
"stored":true,
"indexed":true,
},
{
"name":"estado",
"type":"string",
"multiValued":false,
"stored":true,
"indexed":true,
},
{     
"name":"vector",
"type":"knn_vector_768",
"indexed":true,
"stored":false
},
{     
"name":"ubicaciones",
"type":"string",
"indexed":true,
"stored":true
"multiValued":true,
},
{     
"name":"comunidades",
"type":"text_custom",
"indexed":true,
"stored":true
"multiValued":true,
},
{     
"name":"sujeto_investigacion",
"type":"string",
"indexed":true,
"stored":true
"multiValued":true,
}
]
}'

#curl -X POST -H "Content-Type: application/json" --data-binary @/home/chronomanteca/Descargas/solr-9.1.1/proyectos.json "http://localhost:8983/solr/proyectos/update?commit=true"


curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/proyectos/update?commit=true&wt=json' -d @/home/documents/proyectos.json