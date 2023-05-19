curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/admin/cores?action=CREATE&name=investigadores&configSet=investigadores'

curl http://solr:8983/solr/investigadores/schema -X POST -H 'Content-type:application/json' --data-binary '{
"add-field" : [
{
"name":"nombre",
"type":"text_general",
"multiValued":false,
"stored":true,
"large":true
},   
{
"name":"unidad_negocio",
"type":"string",
"multiValued":false,
"stored":true,
"large":true
},  
{
"name":"departamento",
"type":"string",
"multiValued":false,
"stored":true,
"large":true
},
{
"name":"grupos",
"type":"text_general",
"indexed":true,
"stored":true,
"multiValued":true
},
{
"name":"proyectos",
"type":"text_general",
"indexed":true,
"stored":true,
"multiValued":true
}
]
}'

#curl -X POST -H "Content-Type: application/json" --data-binary @/home/chronomanteca/Descargas/solr-9.1.1/proyectos.json "http://localhost:8983/solr/proyectos/update?commit=true"


curl -X POST -H 'Content-Type: application/json' 'http://solr:8983/solr/investigadores/update?commit=true&wt=json' -d @/home/documents/researchers.json