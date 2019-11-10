## Mapping
mapping类似数据库中schema的定义
* 定义字段的数据类型
* 字段倒排索引相关配置，比如Analyzed or Not Analyzed, Analyzer
dynamic mapping，针对字符串类型，会设置为text，并添加keyword指字段.
获取某个字段的mapping
```
get huapp-2019.09.17/_mapping/field/message
```


## Text vs Keyword
* Text: 全文本，会被进行分词，比如message字段.
* Keyword: 精确词， 不会被分词，比如tags字段等

## 修改固定field的analyzer
```
{
  "mappings": {
    "doc": {
      "_meta": {
        "version": "1.0.0"
      },
      "date_detection": true,
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text",
          "analyzer": "simple"
        },
        "source": {
          "type": "keyword"
        },
        "tags": {
          "type": "keyword"
        }
      }
    }
  },
  "order": 1,
  "settings": {
    "index.mapping.total_fields.limit": 10000,
    "index.refresh_interval": "5s",
    "index.number_of_replicas": 0,
    "index.number_of_shards": 3
  },
  "index_patterns": ["huapp*"]
}
```
