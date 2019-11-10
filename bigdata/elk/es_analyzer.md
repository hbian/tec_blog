### standard analyzer
ELK 默认的analyzer为standard analyzer, 该analyzer的问题为不会针对. dot进行分词，结果针对日志中的报错信息搜索需要进行完整的整词搜索。例如搜索"test"无法匹配到"com.test.ama.error"


### simple analyzer
Simple analyzer可以解决standard analyzer针对.分词的问题, 但是所有的数字在分词的时候都会被忽略.
```
POST _analyze
{
  "analyzer": "simple",
  "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
}
```

### pattern analyzer
现在比较理想的方案是用pattern analyzer， 可以针对 . - 等, the default pattern is \W+, this is equivalent to the set [^a-zA-Z0-9_].