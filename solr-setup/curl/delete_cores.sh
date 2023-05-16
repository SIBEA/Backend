
curl -X POST -H 'Content-Type: application/json' --data-binary '{"delete":{"query":"*:*" }}' http://solr:8983/solr/proyectos/update
curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=proyectos&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"




#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=grupos&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=investigadores&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"





#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_minilm_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_mpnet_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v1_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v2_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_minilm_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_mpnet_cosine&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_minilm_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_mpnet_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v1_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v2_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_minilm_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_mpnet_dot&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_minilm_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_mpnet_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v1_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_distiluse_v2_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_minilm_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
#curl -X DELETE "http://solr:8983/solr/admin/cores?action=UNLOAD&core=model_multilingual_mpnet_euclidean&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"