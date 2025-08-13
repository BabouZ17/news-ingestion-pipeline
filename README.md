# news-ingestion-pipeline
The aim of this project is to build an ingestion pipeline for news. The system has to be able to ingest news on the fly, rank them and display them.

## System design

### High level design

### Ads filtering

### Search / Retrieval of news
The design supports three ways of retrieving the news:
| Retrieval type | Description |
| -------------- | ----------- |
| keyword | Opensearch uses a BM25 algorithm to rank documents which basically gives higher points when the query terms are frequently used [more details](https://docs.opensearch.org/latest/search-plugins/keyword-search/) |
| semantic | The semantic search uses the embeddings computed to make an approximate knn search. More semantically close text chunks in news will have a higher cosine similarity and then rank higher in the result. |
| hybrid | The hybrid search leverages the semantic searches but add boosting to the result. The "published_at" field of the news is boosted to move news 1 day old higher in the reponse |

## How to setup

### Pre-requisites
For the project to run, you will have to have [docker compose](https://docs.docker.com/compose/install/linux/) installed on your environment.

First, you will need [docker engine and docker-cli](https://docs.docker.com/engine/install/) installed.

### Starting / Shuting down
To start the project, run the following:
```
docker compose up --build
```

To stop it:
```
docker compose stop
```

### Kafka topic
First, the project has to be up.

#### List topics
To list existing topics, run the following command:
```
docker exec -it kafka kafka-topics.sh --list --bootstrap-server kafka:9092
```

#### Create topic
The project needs one kafka topic to be created. If you do not want to change the default ("news"), create it by doing:
```
docker exec -it kafka kafka-topics.sh --create --topic news --partitions 3 --bootstrap-server kafka:9092
```

### Kafka UI
Feel free to use Kafbat UI to see what is happening on the kafka level.
You can access it on http://localhost:8080

### Opensearch index
The different embeddings are stored on an opensearch index. To create it,
make a GET HTTP call on the endpoint http://localhost:8002/api/news/createIndex

### OpenAI API Key
You will need a valid OPENAI Api Key to run the project. Just replace the "REPLACE_BY_YOURS" in the docker-compose.yml file by your key.

## Technical details
Find bellow the different services information.

| Service name  | Description | Openapi url |
| ------------  | ----------- | ----------- |
| fake-news-api  | A dummy api service exposing a few news.  | http://localhost:8000/docs |
| news-scheduler  | Service responsible for dispatching news jobs on kafka topic. It can either schedule news jobs or accept dynamic queries using its REST API  | http://localhost:8001/docs |
| news-fetcher | Service responsible for downloading news content. It is listening on kafka topics. | Not applicable |
| news-api | Service responsible for managing news, creating index and making searches | http://localhost:8002/docs |
| news-appi-ui | A little streamlit application to run different types of searches (keyword, semantic, hybrid) | http://localhost:8081/docs |
| kafba ui | Dashboard to interact with kafka cluster | http://localhost:8080 |
| opensearch-dashboards | Dashboard to interact with opensearch indices - PS: username: admin, password: F*ax3Q(8t55O | http://localhost:5601 |


### Remarks / Possible improvements