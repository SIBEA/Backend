#Deleting cores

docker exec -it solr bash /home/setup/delete_cores.sh 

#Initializing and indexing files

docker exec -it solr bash /home/setup/solr_startup_normalized_cosine.sh 

docker exec -it solr bash /home/setup/solr_startup_normalized_dot_product.sh 

docker exec -it solr bash /home/setup/solr_startup_normalized_euclidian.sh 