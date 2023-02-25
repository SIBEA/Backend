
# **Backend**
 

## **Informacion de Solr**

---
Version de Solr usada: 9.1.1:\
https://solr.apache.org/downloads.html Descargar los binarios

## **Comandos:**
- **bin/solr start** : Inicia solr en el puerto 8983 por defecto
- **bin/solr -c create <CORE_NAME>** : Crea un core con el nombre especificado.
- **bin/solr -c delete <CORE_NAME>**: Elimina el core especificado
- **bin/post -c <CORE_NAME> <JSON_FILE_ROUTE>**: Indexa los documentos contenidos en el archivo json ubicado en la ruta establecida al core indicado.

## **El directorio Solr commands:**

En este directorio se encuentran comandos que pueden ser de utilidad al automatizar, de manera general existen dos tipos de archivos:\
### **1. Archivos de creacion (solr_startup_*_.sh)**

Se encargan de configurar el proceso de creacion de nucleos usando el siguiente proceso:\

1. Crean uno (o varios) nucleos:
   ```
   bin/solr create -c <Nombre_core>
   ```
2. Configuran el schema del core:
    ```
    curl http://localhost:8983/solr/model_minilm/schema -X POST -H 'Content-type:application/json' --data-binary '{
    "add-field-type" : {
    "name":"knn_vector_384",
    "class":"solr.DenseVectorField",
    "vectorDimension":384,
    "similarityFunction":"cosine",
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
    ```
En este proceso ocurren dos cosas importantes
- Se configura el field-type "DenseVector"
- Se asigna el anterior field-type al campo "vector", el cual contiene el vector generado a partir del corpus por el modelo respectivo\
(Para mayor detalle consultar: https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html)
  
NOTA: los demas campos corresponden al restante de los parametros de cada documento, se pueden agregar/quitar de ser necesario. 


### **2. Archivo de eliminacion**

Este unicamente se encarga de borrar los nucleos de la instancia de solr especificada mediante el comando delete.

El directorio viene incluido con los siguientes archivos:

 Comando | Funcion de similitud |
| ----------- | ----------- |
| solr_startup_normalized_cosine | similitud de cosenos |
| solr_startup_normalized_euclidean | distancia euclideana |
| solr_startup_normalized_dot_product | producto punto |

Lo unico que varia es la funcion de similitud que emplea solr para buscar los vectores mas cercanos al query

## **El directorio Solr vectores:**

Contiene dos subdirectorios:

- Normalized: Los vectores en este directorio estan normalizados, ademas el dataset se limpio (Eliminacion de tipo_proyecto AJI)

- Not Normalized: Los vectores en este directorio no estan normalizados, y usan el dataset original (sin la eliminacion de tipo_proyecto AJI)

Cada archivo json tiene el nombre del modeo que se empleo para generar los embeddings.

---

## **Proceso de configuracion de solr**

1. Descargar y extraer los archivos binarios usando el enlace proveido
2. Mover los archivos del directorio "solr_commands" a la raiz de los binarios de solr.
3. Configurar la ruta de los archivos JSON en el archivo que se desea ejecutar.
4. Ejecutar el archivo sh de su preferencia
   
Ejemplo:

 	``` 
    ./solr_startup_regular_cosine.sh
    ``` 




