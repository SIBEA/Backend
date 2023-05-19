
curl -X POST -H 'Content-Type: application/json' --data-binary '{"delete":{"query":"*:*" }}' http://solr:8983/solr/proyectos/update
curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=proyectos&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"



curl -X POST -H 'Content-Type: application/json' --data-binary '{"delete":{"query":"*:*" }}' http://solr:8983/solr/grupos/update
curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=grupos&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"


curl -X POST -H 'Content-Type: application/json' --data-binary '{"delete":{"query":"*:*" }}' http://solr:8983/solr/investigadores/update
curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=investigadores&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
