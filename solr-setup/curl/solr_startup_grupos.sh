curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=grupos&configSet=grupos'

curl http://solr:8983/solr/grupos/schema -X POST -H 'Content-Type: application/json' --data-binary '{
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


curl http://solr:8983/solr/grupos/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field" : [
{
"name":"nombre",
"type":"text_custom",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"lider",
"type":"string",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"email_lider",
"type":"string",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"url_gruplac",
"type":"string",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"investigadores",
"type":"text_custom",
"indexed":true,
"stored":true,
"multiValued":true
},
{
"name":"proyectos",
"type":"text_custom",
"indexed":true,
"stored":true,
"multiValued":true
}
]
}'

#curl -X POST -H "Content-Type: application/json" --data-binary @/home/chronomanteca/Descargas/solr-9.1.1/proyectos.json "http://localhost:8983/solr/proyectos/update?commit=true"


curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/grupos/update?commit=true&wt=json' -d @/home/documents/groups.json