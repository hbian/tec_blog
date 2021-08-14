## ELK 大型多行日志的处理
https://www.cnblogs.com/liujiliang/p/12937637.html
https://www.cnblogs.com/doubletree/p/4264969.html

Filebeat -> kafka -> logstash  -> es -> kibana, 现在的问题主要是在Filebeat和kafka

Filebeat:
multiline.max_lines: 可以合并成一个事件的最大行数。如果一个多行消息包含的行数超过max_lines，则超过的行被丢弃,默认是500。现在遇到的问题主要是在这里，超过500行的日志数据直接被抛弃了。

Kafka broker：
Kafka设计的初衷是迅速处理短小的消息，一般10K大小的消息吞吐性能最好（可参见LinkedIn的kafka性能测试）
* message.max.bytes (默认:1000000 953K) – broker能接收消息的最大字节数，这个值应该比消费端的fetch.message.max.bytes更小才对，否则broker就会因为消费端无法使用这个消息而挂起。
* log.segment.bytes (默认: 1GB) – kafka数据文件的大小，确保这个数值大于一个消息的长度。一般说来使用默认值即可（一般一个消息很难大于1G，因为这是一个消息系统，而不是文件系统）。
* replica.fetch.max.bytes (默认: 1MB) – broker可复制的消息的最大字节数。这个值应该比message.max.bytes大，否则broker会接收此消息，但无法将此消息复制出去，从而造成数据丢失。


Kafka Consumer :
 fetch.message.max.bytes (默认 1MB) – 消费者能读取的最大消息。这个值应该大于或等于message.max.bytes。