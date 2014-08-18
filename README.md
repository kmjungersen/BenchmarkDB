# Database Benchmarking

This application is intended to help you benchmark a database of your choice very simply and easily.  Simply follow the specified steps to build a module of your own and then you can see how it stacks up to other similar databases!

## Building a module

1. Create a new file for the desired DB
2. Import the template class from `benchmark_template.py` and structure as follows:
    ``` python
    from benchmark_template.py import BenchmarkDatabase


    class MyCoolNewDatabase(BenchmarkDatabase):

    ...
    ```
3. Build the module!  The functions for the module must match the super class structure and parameters.  Pay special attention to the exact operations of each function!
4. Make/ borrow ansible roles for deployment of the DB to 1 or several vagrant boxes.  All existing examples are for sharded clusters, which use either 3 or 4 nodes in the cluster, however if you want to benchmark a single instance of a DB you're welcome to do so.
5. Test ruthlessly!  Make sure your module is performing the read, write, and setup functions exactly as they should.  Verify the records are being written properly and then read properly too.  Any mistakes in this area will make your data worthless!
6. Submit a PR with your finished module!  If you've taken the time to build a module to benchamrk a DB, go ahead and clean up the module before submitting a PR to share it with everyone.  For more info, please see `CONTRIBUTING.md`.
