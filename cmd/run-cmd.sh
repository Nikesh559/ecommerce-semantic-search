docker run -d --name qdrant-vector-db -p 6333:6333 -p 6334:6334 -v /qdrant_dir:/qdrant/storage qdrant/qdrant:latest
docker run -d --name kafka -p 9092:9092 \
-e KAFKA_ZOOKEEPER_CONNECT=host.docker.internal:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
confluentinc/cp-kafka


bin/kafka-console-consumer \ --topic products \ --bootstrap-server localhost:9092

bin/kafka-console-consumer \ --topic products \ --bootstrap-server localhost:9092 \ --property print.key=true \ --property key.separator=" : "

bin/kafka-console-producer \ --topic products \ --bootstrap-server localhost:9092

bin/kafka-console-producer \
--topic products \
--bootstrap-server localhost:9092

./bin/kafka-topics --delete --topic products --bootstrap-server localhost:9092
