## Delete by query
为了节省硬盘存储空间，我们需要删除一个index下的某些tags， 
可以使用 docs-delete-by-query
The simplest usage of _delete_by_query just performs a deletion on every document that match a query. Here is the API:
```
POST test/_delete_by_query
{
  "query": { 
    "match": {
      "message": "some message"
    }
  }
}
```
删除某个tag
```
POST test-2019.06.11/_delete_by_query
{
  "query": { 
    "match": {
      "tags": "testapp"
    }
  }
}
```

删除会比较耗时，删除后会发现Segment Count和Document Count会减少，但是disk没有变化， 这是因为：In Lucene, a document is not deleted from a segment, just marked as deleted.

需要调用forcemerge api，  
only_expunge_deletes：Should the merge process only expunge segments with deletes in it. During a merge process of segments, a new segment is created that does not have those deletes. This flag allows to only merge segments that have deletes. Defaults to false. 
```
POST /test-2019.07.01/_forcemerge?only_expunge_deletes=true
```



## cluster_block_exception
retrying failed action with response code: 403 ({"type"=>"cluster_block_exception", "reason"=>"blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];"}) 修改所在index的read_only_allow_delete配置 PUT air-2019.08.07/_settings { "index": { "blocks": { "read_only_allow_delete": "false" } } }

如果无法找到有问题的index
PUT _all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

比如如果是url shorter无法使用
PUT .kibana/_settings 
{ "index": { "blocks": {"read_only_allow_delete": "false" } } }

