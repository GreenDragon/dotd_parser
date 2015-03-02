mysqldump dotd_parser raw_log > raw_log.sql
remove drop table commands
%s/raw_log/logs/g

mysql dotd_parser < raw_log.sql
