## Sqoop error with Oracle
sqoop 默认没有oracle的driver，需要ojdbc6.jar连接oracle 11g，
将driver防止parcel jars目录下，/data/cdh/parcels/CDH-6.0.1-1.cdh6.0.1.p0.590678/jars/ 如果继续报以下无法找到driver的问题：
Could not load db driver class: oracle.jdbc.OracleDriver
Place the odbc6.jar in sqoop/lib and retry
cp /data/cdh/parcels/CDH-6.0.1-1.cdh6.0.1.p0.590678/jars/ojdbc6.jar /data/cdh/parcels/CDH-6.0.1-1.cdh6.0.1.p0.590678/lib/sqoop/lib


## python mysql client install
需要先安装yum -y install mysql-devel, 否则会有mysql_config not found错误，
然后再安装pipenv install mysqlclient==1.4.6
