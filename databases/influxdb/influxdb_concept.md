在influxdb中tags是indexed， Fileds是没有indexed。通过fileds中的值过滤的query会扫描所有的数据，这会非常的慢。
但是大量数据的时候如果tags的值非常的多，也会导致内存暴涨，influxdb有可能挂掉，遇到过的问题是在做nginx的日志处理时，将ip作为tags，方面后面进行搜索排序，在ip很多的的时候(100,000+)， 几天后会发现内存使用增长的非常快，最终导致内存不足重启。为了解决这个问题好，把ip放在fileds中进行处理，针对ip的统计排序这类操作，将数据从influxdb读出后用spark进行二次处理，不直接在influxdb中进行处理。



## Fields
It’s also important to note that fields are not indexed. Queries that use field values as filters must scan all values that match the other conditions in the query. As a result, those queries are not performant relative to queries on tags (more on tags below). In general, fields should not contain commonly-queried metadata.

## Series
 In InfluxDB, a series is the collection of data that share a retention policy, measurement, and tag set
 
## Encouraged schema design
 In general, your queries should guide what gets stored as a tag and what gets stored as a field:

Store data in tags if they’re commonly-queried meta data
**Store data in tags if you plan to use them with GROUP BY()**
Store data in fields if you plan to use them with an InfluxQL function
**Store data in fields if you need them to be something other than a string - tag values are always interpreted as strings**