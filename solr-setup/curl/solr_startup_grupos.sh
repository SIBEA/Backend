curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=grupos&configSet=grupos'

curl http://solr:8983/solr/grupos/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field" : [
{
"name":"nombre",
"type":"text_general",
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
"type":"text_general",
"indexed":true,
"stored":false,
"multiValued":true
},
{
"name":"proyectos",
"type":"text_general",
"indexed":true,
"stored":false,
"multiValued":true
}
]
}'

#curl -X POST -H "Content-Type: application/json" --data-binary @/home/chronomanteca/Descargas/solr-9.1.1/proyectos.json "http://localhost:8983/solr/proyectos/update?commit=true"


curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/grupos/update?commit=true&wt=json' -d @/home/documents/groups.json