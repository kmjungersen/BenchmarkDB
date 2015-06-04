DATABASE BENCHMARKING REPORT - POSTGRESQL - 1000 Trials
=========================================

This report has been automatically generated from a Benchmarking application
built by [Kurtis Jungersen](http://kmjungersen.com).  The source behind the application can be found on the [project's GitHub.](https://github.com/kmjungersen/DB-Benchmarking)

TIME AND DATE
=============

Thu, 04 Jun, 2015 15:37:32


RESULTS
=======

After using these parameters:

| Parameter                          | Value      |
|:-----------------------------------|:-----------|
| Database Tested                    | POSTGRESQL |
| Number of Trials                   | 1000       |
| Length of Each Entry Field         | 10         |
| Number of Nodes in Cluster         | 3          |
| # of StDev's Displayed in Graphs   | 1          |
| Range of Rolling Average in Graphs | 100        |
| Split Reads and Writes             | True       |
| Debug Mode                         | False      |
| Chaos Mode (Random Reads)          | False      |

These results were obtained:

| Operation   |   Average |   St. Dev. |   Max Time |   Min Time |   Range |
|:------------|----------:|-----------:|-----------:|-----------:|--------:|
| Writes      |   0.00156 |    0.01193 |    0.30336 |    0.00071 | 0.30265 |
| Reads       |   0.00125 |    0.01522 |    0.30254 |    0.00031 | 0.30223 |

This plot shows the normalized speeds of reads and writes over the course of the benchmark.  The data was normalized (i.e. any data points beyond 3 standard deviations of the mean were excluded).

![Alt text](images/POSTGRESQL-Jun04-2015-15:37:32-rw.png "rw")

This plot shows a histogram which describes the general distribution of the data.

![Alt text](images/POSTGRESQL-Jun04-2015-15:37:32-stats.png "stats")

This plot shows the running averages for read and write speeds over the course of the benchmark.

![Alt text](images/POSTGRESQL-Jun04-2015-15:37:32-running_averages.png "running_averages")