## Replace timestamp by logstash system time
因应用服务器时间无法修改，所以只能在logstash处进行替换
```
filter {

  mutate {
    add_field => { "realtimestamp" => "%{@timestamp}" }
  }

  ruby {
    code => "event.set('logstash_processed_at', Time.now());"
  }

  mutate {
    convert => { "logstash_processed_at" => "string" }
  }

  date {
    match => [ "logstash_processed_at", "ISO8601" ]
    target => "@timestamp"
  }
}

```