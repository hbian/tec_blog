## Sqoop export数据重复的问题
使用sqoop export 到mysql中时，如果使用
```
--update-mode allowinsert \
--update-key "dt,airline" \
```
--update-key指定的字段在数据库表中必须是唯一非空的PRIMARY KEY，这样此模式才能实现数据库表中已存在的数据进行更新，不存在的数据进行插入。否则这个模式会将所有数据都以insert语句插入数据库中。
如果表没有主键，没有唯一非空字段，那么在使用allowinsert模式的时候，即使指定了--update-key的字段为dt,airline，那么在进行导出的时候，Sqoop也不会去检查dt,airline字段，而是直接选择insert语句进行插入，那么数据仍然会重复插入。
也就是说在建mysql表时需要设置--update-key dt,airline 为 PRIMARY KEY
```
#Create mysql table
PRIMARY KEY (`airline`, `dt`)

#sqoop export
--update-mode allowinsert \
--update-key "dt,airline" \
```