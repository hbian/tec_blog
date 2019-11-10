##Search
默认只会返回前10个hits,指定size参数可以
```
POST oracle-2019.08.*/_search
{   "size": 20,
    "query": {
        "match_phrase" : {
          "message": {
            "query": "ora"
          }
        }
    }
}
```


### Serach by time
```
POST oracle*/_search
{
    "query": {
        "range" : {
            "@timestamp" : {
                "gte" : "now-10m/m"
            }
        }
    }
}

#或者用constant_score, filter
POST oracle*/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-10m/m"
          }
        }
      }
    }
  }
}
```

### Return selected fileds
加上 "_source": ["message"]， 字段后，返回结果_source将只含有message字段，方便搜索结果过滤
```
POST oracle*/_search
{ "_source": ["message", "tags"],
    "query": {
        "range" : {
            "@timestamp" : {
                "gte" : "now-10m/m"
            }
        }
    }

}
```

### Sort the result
```
POST oracle*/_search
{ "_source": ["message", "tags", "@timestamp"],
  "sort": [{"@timestamp" : "desc"}],
    "query": {
        "range" : {
            "@timestamp" : {
                "gte" : "now-10m/m"
            }
        }
    }

}
```

### Match
```
POST oracle-2019.09.06/_search
{ "_source": ["message", "tags", "@timestamp"],
  "sort": [{"@timestamp" : "desc"}],
    "query": {
        "match" : {
          "message": "124380 online"
        }
        }
    }
}
```
默认的是OR的查询条件，也就是messager含有124380或者online,可以使用如下语法进行AND查询
```
POST oracle-2019.09.06/_search
{
    "query": {
        "match" : {
          "message": {
            "query": "124380 online",
            "operator": "AND"
          }
        }
        }
    }
}
```

### Match phrase

```
LNS: Standby redo logfile selected for thread 2 sequence 124380 for destination LOG_ARCHIVE_DEST_2

POST oracle-2019.09.06/_search
{
    "query": {
        "match_phrase" : {
          "message": {
            "query": "124380 destination"
          }
        }
    }
}
```
Match phrase 的query中的词必须按顺序出现，搜索124380 destination会什么都搜索不到， 124380 for destination才能搜索到正确结果
使用"slop"字段可以允许中间插入单词,如下的请求就可以搜索到124380 for destination
```
POST oracle-2019.09.06/_search
{
    "query": {
        "match_phrase" : {
          "message": {
            "query": "124380 destination",
            "slop": 1
          }
        }
    }
}
```


## Term 查询
Term: 作为表达语义的最小单位，在输入es进行查询时，es不会捉分词处理，会将输入作为一个整体进行搜索。
```
POST oracle-2019.09.09/_search
{   
    "query": {
        "term" : {
          "tags": {
            "value": "Pro"
          }
        }
    }
}
```
这个查询的返回结果为0，因为Pro没有进行任何处理，大写的P于索引中的小写不匹配，改为pro后就有结果了。
将查询改为constant_score filter,可以避免算分，使用缓存
```
POST oracle-2019.09.09/_search
{   
    "query": {
      "constant_score": {
        "filter": {        
          "term" : {
          "tags": "pro"
        }
      }
    }
  }
}
```

如果希望进行精确匹配，可以将字段设为keyword，keyword在索引时不会进行分词处理。

结构化收据：日期，布尔类型，数字运行环境，以及一些有固定集合的标签，比如博客的标签，运行环境标签，针对这种数据用term查询更适合。

### 全文本查询
包括 match query, match phrase query, query string query.在查询时会先进行分词，拆分成term,然后对每个词项term进行查询，最后合并结果。

## Bool 查询
must, shouold, must_not, filter 
```
POST oracle*/_search
{
  "query": {
    "bool": {
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-4d/d"
          }
        }
      },
      "must": [
        {
          "match_phrase": {
            "message": {
              "query": "ora"
            }
          }
        },
        {
          "term": {
            "tags": "pro"
          }
        }
      ]
    }
  }
```