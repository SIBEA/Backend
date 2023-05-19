rm -r /var/solr/data
mkdir -p /var/solr/data
mkdir -p /var/solr/data/configsets

cp -r ./server/solr/configsets/_default /var/solr/data/configsets/proyectos
cp -r ./server/solr/configsets/_default /var/solr/data/configsets/grupos
cp -r ./server/solr/configsets/_default /var/solr/data/configsets/investigadores

solr-foreground