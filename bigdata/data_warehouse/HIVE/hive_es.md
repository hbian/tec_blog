### Hive ES installation
Make elasticsearch-hadoop jar available in the Hive classpath. Depending on your options, there are various ways to achieve that. Use ADD command to add files, jars (what we want) or archives to the classpath, the command expects a proper URI that can be found either on the local file-system or remotely. Typically it’s best to use a distributed file-system (like HDFS or Amazon S3) and use that since the script might be executed on various machines.

### Hive table mapping

By default, elasticsearch-hadoop uses the Hive table schema to map the data in Elasticsearch, using both the field names and types in the process. There are cases however when the names in Hive cannot be used with Elasticsearch (the field name can contain characters accepted by Elasticsearch but not by Hive). For such cases, one can use the es.mapping.names setting which accepts a comma-separated list of mapped names in the following format: Hive field name:Elasticsearch field name.比如说像@timestamp这种可以在导入时进行转换。

Hive is case insensitive while Elasticsearch is not. The loss of information can create invalid queries (as the column in Hive might not match the one in Elasticsearch). To avoid this, elasticsearch-hadoop will always convert Hive column names to lower-case. This being said, it is recommended to use the default Hive style and use upper-case names only for Hive commands and avoid mixed-case names.

Hive treats missing values through a special value NULL as indicated here. This means that when running an incorrect query (with incorrect or non-existing field names) the Hive tables will be populated with NULL instead of throwing an exception.