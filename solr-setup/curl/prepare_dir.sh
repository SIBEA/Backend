rm -r /var/solr/data
mkdir -p /var/solr/data
mkdir -p /var/solr/data/configsets

cp -r ./server/solr/configsets/_default /var/solr/data/configsets/proyectos
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/grupos
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/investigadores



#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_minilm_cosine
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_mpnet_cosine
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v1_cosine
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v2_cosine
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_minilm_cosine
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_mpnet_cosine

#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_minilm_dot
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_mpnet_dot
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v1_dot
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v2_dot
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_minilm_dot
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_mpnet_dot

#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_minilm_euclidean
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_mpnet_euclidean
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v1_euclidean
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_distiluse_v2_euclidean
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_minilm_euclidean
#cp -r ./server/solr/configsets/_default /var/solr/data/configsets/model_multilingual_mpnet_euclidean

solr-foreground