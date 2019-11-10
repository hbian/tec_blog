## Quick start
```
su - kafka
./confluent start kafka


bin/kafka-topics --create --zookeeper localhost:2181 \
  --replication-factor 1 --partitions 1 --topic users

bin/kafka-console-consumer --topic hu --zookeeper localhost:2181 --from-beginning

```