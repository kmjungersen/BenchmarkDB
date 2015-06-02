# PostgreSQL

This module is for testing PostgreSQL version 9.3 on CentOS 6.x.  There are some important features and modifications to note about this module:

* The text and numerical field lengths were cut in half due to integer limitations in SQL
* This is NOT a truly horizontal scaling of postgreSQL!  This is merely one potential use-case of a "sharded" SQL.  This was achieved through chunking a data set and then assigning each node a chunk.  This reduces the load on each node, however is merely an imitation of No-SQL horizontal scaling.  