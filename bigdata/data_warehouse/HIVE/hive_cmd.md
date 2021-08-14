### Hive tables
describe extended <table_name>;

describe formatted  <table_name>;

## Hive Metastore tables:
"TBLS" stores the information of Hive tables.
"PARTITIONS" stores the information of Hive table partitions.
"SDS" stores the information of storage location, input and output formats, SERDE etc.
Both "TBLS" and "PARTITIONS" have a foreign key referencing to SDS(SD_ID).

### To list table location:
```
select TBLS.TBL_NAME,SDS.LOCATION
from SDS,TBLS
where TBLS.SD_ID = SDS.SD_ID;
```
### To list table partition location:
```
select TBLS.TBL_NAME,PARTITIONS.PART_NAME,SDS.LOCATION
from SDS,TBLS,PARTITIONS
where PARTITIONS.SD_ID = SDS.SD_ID
and TBLS.TBL_ID=PARTITIONS.TBL_ID
order by 1,2;
```

### 查看hive元数据
```
analyze table [table_name] compute statistics; 
analyze table [table_name] partition(分区列) compute statistics;
analyze table [table_name] partition(分区列) compute statistics for columns;
## 不扫描全表，只取numFiles， totalSize
analyze table [table_name] compute statistics noscan;
```