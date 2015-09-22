# MongoDB
This document details different scenarios of usage for MongoDB and how Mongo handles them.

## Replication set - 1 of 3 nodes forcefully shutdown
This was tested using a sharded replication set.  After the cluster was up and running, a single node was taken offline forcefully.  The cluster was still operational and continued to accept reads and writes after the shutdown.  *One important note,* however, is that if the primary member of the replication set goes down, the cluster is unable to function.
