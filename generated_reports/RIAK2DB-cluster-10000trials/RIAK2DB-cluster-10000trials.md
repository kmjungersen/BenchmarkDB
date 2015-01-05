DATABASE BENCHMARKING REPORT - RIAK2 - 10000 Trials
=========================================

This report has been automatically generated from a Benchmarking application
built by [Kurtis Jungersen](http://kmjungersen.com).  The source behind the application can be found on the [project's GitHub.](https://github.com/kmjungersen/DB-Benchmarking)

TIME AND DATE
=============

Wed, 17 Dec, 2014 15:24:21


RESULTS
=======

After using these parameters:

| Parameter                        | Value   |
|:---------------------------------|:--------|
| Database Tested                  | RIAK2   |
| Number of Trials                 | 10000   |
| Length of Each Entry Field       | 10      |
| Number of Nodes in Cluster       | 3       |
| # of StDev's Displayed in Graphs | 3       |
| Split Reads and Writes           | True    |
| Debug Mode                       | False   |
| Chaos Mode (Random Reads)        | True    |

These results were obtained:

| Operation   |   Average |   St. Dev. |   Max Time |   Min Time |   Range |
|:------------|----------:|-----------:|-----------:|-----------:|--------:|
| Writes      |   0.00510 |    0.00191 |    0.06833 |    0.00226 | 0.06607 |
| Reads       |   0.00394 |    0.00142 |    0.02211 |    0.00144 | 0.02067 |

This plot shows the normalized speeds of reads and writes over the course of the benchmark.  The data was normalized (i.e. any data points beyond 3 standard deviations of the mean were excluded).

![Alt text](images/RIAK2-Dec17-2014-15:24:21-rw.png "rw")

This plot shows a histogram which describes the general distribution of the data.

![Alt text](images/RIAK2-Dec17-2014-15:24:21-stats.png "stats")

This plot shows the running averages for read and write speeds over the course of the benchmark.

![Alt text](images/RIAK2-Dec17-2014-15:24:21-running_averages.png "running_averages")