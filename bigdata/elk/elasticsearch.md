## Delete by query
为了节省硬盘存储空间，我们需要删除一个index下的某些tags， 
可以使用 docs-delete-by-query
The simplest usage of _delete_by_query just performs a deletion on every document that match a query. Here is the API:
```
POST twitter/_delete_by_query
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
POST air-2019.06.11/_delete_by_query
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