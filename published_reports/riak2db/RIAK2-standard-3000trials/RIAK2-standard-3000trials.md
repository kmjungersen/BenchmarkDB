DATABASE BENCHMARKING REPORT - RIAK2 - 3000 Trials
=========================================

This report has been automatically generated from a Benchmarking application
built by [Kurtis Jungersen](http://kmjungersen.com).  The source behind the application can be found on the [project's GitHub.](https://github.com/kmjungersen/DB-Benchmarking)

TIME AND DATE
=============

Thu, 13 Nov, 2014 17:59:17


RESULTS
=======

After using these parameters:

| Parameter                  | Value   |
|:---------------------------|:--------|
| Database Tested            | RIAK2   |
| Number of Trials           | 3000    |
| Length of Each Entry Field | 10      |
| Number of Nodes in Cluster | 3       |
| Split Reads and Writes     | True    |
| Debug Mode                 | False   |
| Chaos Mode (Random Reads)  | True    |

These results were obtained:

| Operation   |   Average |   St. Dev. |   Max Time |   Min Time |   Range |
|:------------|----------:|-----------:|-----------:|-----------:|--------:|
| Writes      |   0.00324 |    0.00279 |    0.15095 |    0.00217 | 0.14878 |
| Reads       |   0.00173 |    0.00060 |    0.01875 |    0.00108 | 0.01766 |

This plot shows the normalized speeds of reads and writes over the course of the benchmark.  The data was normalized (i.e. any data points beyond 3 standard deviations of the mean were excluded).

![Alt text](images/RIAK2-Nov13-2014-17:59:17-rw.png "rw")

This plot shows a histogram which describes the general distribution of the data.

![Alt text](images/RIAK2-Nov13-2014-17:59:17-stats.png "stats")

This plot shows the running averages for read and write speeds over the course of the benchmark.

![Alt text](images/RIAK2-Nov13-2014-17:59:17-running_averages.png "running_averages")

Note: If any outliers were obtained in this benchmark, they will displayed here:

| Operation   |   Trial Number |      Value |
|:------------|---------------:|-----------:|
| Write       |              0 | 0.150947   |
| Write       |           2318 | 0.011761   |
| Read        |              0 | 0.0187471  |
| Read        |             18 | 0.00383496 |
| Read        |             74 | 0.003901   |
| Read        |            518 | 0.00425982 |
| Read        |            519 | 0.00406289 |
| Read        |            521 | 0.00368214 |
| Read        |            522 | 0.00363493 |
| Read        |            523 | 0.00409603 |
| Read        |            524 | 0.00426888 |
| Read        |            525 | 0.00413895 |
| Read        |            526 | 0.00439286 |
| Read        |            527 | 0.00441694 |
| Read        |            534 | 0.00370097 |
| Read        |           1130 | 0.00418711 |
| Read        |           1131 | 0.004915   |
| Read        |           1134 | 0.00433302 |
| Read        |           1135 | 0.003896   |
| Read        |           1136 | 0.00363493 |
| Read        |           1137 | 0.00362301 |
| Read        |           1138 | 0.00411391 |
| Read        |           1139 | 0.00409603 |
| Read        |           1140 | 0.00491786 |
| Read        |           1141 | 0.00436211 |
| Read        |           1142 | 0.00355983 |
| Read        |           1146 | 0.0042119  |
| Read        |           1148 | 0.00357795 |
| Read        |           1745 | 0.00434494 |
| Read        |           1746 | 0.00411296 |
| Read        |           1750 | 0.00391293 |
| Read        |           1751 | 0.00385094 |
| Read        |           1752 | 0.00384808 |
| Read        |           1754 | 0.00361013 |
| Read        |           1755 | 0.00389791 |
| Read        |           1756 | 0.00363278 |
| Read        |           1757 | 0.0048759  |
| Read        |           1758 | 0.00430989 |
| Read        |           1759 | 0.00355792 |
| Read        |           1763 | 0.00396299 |
| Read        |           1866 | 0.00523615 |
| Read        |           1867 | 0.00479102 |
| Read        |           1869 | 0.00374198 |
| Read        |           1871 | 0.00368309 |
| Read        |           1873 | 0.00440502 |
| Read        |           2348 | 0.00366092 |
| Read        |           2349 | 0.00396204 |
| Read        |           2352 | 0.00450683 |
| Read        |           2353 | 0.00402808 |
| Read        |           2354 | 0.00408578 |
| Read        |           2356 | 0.00418997 |
| Read        |           2357 | 0.00363708 |
| Read        |           2359 | 0.0039289  |
| Read        |           2360 | 0.00447989 |
| Read        |           2363 | 0.00357604 |
| Read        |           2364 | 0.00414014 |
| Read        |           2601 | 0.00363898 |
| Read        |           2955 | 0.00438094 |
| Read        |           2956 | 0.00478888 |
| Read        |           2958 | 0.00375819 |
| Read        |           2959 | 0.0038898  |
| Read        |           2960 | 0.00383687 |
| Read        |           2961 | 0.00470805 |
| Read        |           2962 | 0.00359893 |
| Read        |           2964 | 0.00426412 |
| Read        |           2967 | 0.0042069  |
| Read        |           2969 | 0.00440907 |
| Read        |           2972 | 0.00401998 |
| Read        |           2973 | 0.00425315 |
| Read        |           2974 | 0.00449896 |
| Read        |           2978 | 0.00353909 |