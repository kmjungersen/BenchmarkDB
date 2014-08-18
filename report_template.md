DATABASE BENCHMARKING REPORT - {database}
=========================================

This report has been automatically generated from a Benchmarking application
built by [Kurtis Jungersen](http://kmjungersen.com).

Results
=======

After using these parameters:

| Parameter                  | Value     |
|----------------------------|-----------|
| Database                   | {database}     |
| Number of Trials           | {trial_number}        |
| Length of Each Entry Field | {entry_length}        |
| Number of Nodes in Cluster | {node_number}         |

These results were obtained:

| Operation | Average | Standard Deviation | Max time | Min time|
|-----------|---------|--------------------|----------|---------|
| Writes    | {write_avg:.4f}  | {write_stdev:.4f}             | {write_max:.4f}   | {write_min:.4f}  |
| Reads     | {read_avg:.4f}  | {read_stdev:.4f}             | {read_max:.4f}   | {read_min:.4f}  |