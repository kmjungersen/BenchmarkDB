# Database Benchmarking

This application is intended to help you benchmark a database of your choice very simply and easily.  Simply follow the specified steps to build a module of your own and then you can see how it stacks up to other similar databases!

## Using the Application

1. Install dependencies from `requirements.txt`.  It's recommended to use a virtual environment.
    ``` bash
    $ cd <path_to_project>/DB-Benchmarking
    $ pip install -r requirements.txt
    ```

2. Deploy vagrant machine(s)
   This procedure is slightly different for every module, so be sure to read the `README` for each one.
3. Run the application!

    ```
    $ python main.py <database_module_name> [options]
    ```

    * General usage information and options:
    ```
    DB Benchmarking Application
    ===========================

    Main.py

    This file houses the core of the application, and is where all of the read/write
    commands are issued from, timed, and all data is analyzed.  Results from the
    trials are printed to the console by default, but can optionally be printed to a
    file to keep a record of.  This is particularly helpful when benchmarking
    multiple DB's in a row to see which one is best for deployment purposes.

        Usage:
            main.py <database> [options]

        Options:
            -h --help           Show this help screen
            -v --verbose        Show verbose output from the application
            -l --list_mods      Outputs a list of available DB modules before running
            -r --report         Option to generate a report file, which will
                                    OVERWRITE any existing reports from the specified
                                    DB in the `generated_reports` directory

            --entry_length=<n>  Specify an entry length [default: 10]
            --trial_number=<n>  Specify the number of reads and writes to make to the
                                    DB to collect data on [default: 100]
    ```

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
