# Contributing

Contributing a module to this application is very simple!

After you build a module, test it rigorously and then please submit a pull request!  Take a close look at the documentation to make sure each function in your module does the exact prescribed functionality.  The basic structure can be seen in `benchmark_template.py`, however we'll briefly look at it here too:

1. Fork the project from `dev`, make a feature branch, and create the module directory
    * Create the directory inside the BenchmarkDB directory: `...BenchmarkDB/BenchmarkDB/<my_new_module>`
    * Name said directory logically: `<my_new_module>db`, e.g. `mongodb` and `riakdb`.  The "db" at the end is **very important!**

        ``` bash
        $ mkdir BenchmarkDB/<my_new_module>db
        ```

2. Move into the directory and create a few important things:

    ``` bash
    # Create the `__init__` file to make this directory a python package
    $ touch __init__.py

    # Create the primary file that will house all of the read/write commands for your db
    $ touch main.py

    # Create the settings and configuration file
    $ touch local.py
    ```

3. Create your deployment automation:

    Use ansible roles or docker to automate the deployment, and provide documentation for use
    

4. Create your primary DB file in `main.py`
    * Due to the nature of the application, you don't need to do any timing, recording, data_compliation, etc.  The wonderful thing is that all you need to do is create this module with a `main.py` that follows the given structure and the rest is done for you.  
    * Therefore, something to keep in mind is that the `main.py` you're creating will **only setup a DB connection, write to the DB, and then read from the DB**.  This makes things really simple to write, and enables us to create a relatively unbiased benchmarking report on various DB's since we're testing them all in the exact same way.
    * More detailed documentation on the specific functionality of each function lives in `benchmark_template.py`, but here is an outline:

        ```python
        from benchmark_template import BenchmarkDatabase
        from <python_library_for_some_db> import SomeClient

        class Benchmark(BenchmarkDatabase):

            def __init__(self, setup=False, verbose=False):
                """ `__init__()` is the entry point of the module, and is where the
                module is set up and prepared for benchmarking.  This class is
                initialized in `main.py` of the main project directory, and is always
                called with the optional parameter `setup=True`.  It defaults to `False`
                for the sole reason of building tests.
        
                :param collection: The collection of the DB which all reads and
                            writes will occur with
                :param setup: A Bool to determine whether or not `setup()` should be
                            called upon initialization or not
                :param trials: The number of trials to be completed.  This is ONLY
                            needed for SQL DB's
                """
                self.trials = trials
        
                if setup:
                    self.setup(collection)

            def setup(self, collection):
                """ This function handles all of the setup operations for the database
                reads and writes.  It is typically called from `__init__()`, although
                not necessarily in the case of tests.  It is crucial that this function
                sets up the client-database connection for use in other functions of this
                class.  A `local.py` file should exist in the module directory and should
                include the IP addresses and ports needed to connect to the DB.
        
                :param collection: The collection or table with which all benchmarks
                            will be run 
                """

                # Do some setup stuff to get the DB client ready to use
                self.client = SomeClient()
                
                ...

            def write(self, data):
                """ This function should only perform a write task, given a document
                to write to the database.
        
                :param data: a dictionary-type document that will be written to the db
                """

                self.client.write(data)

            def read(self, index):
                """ This function should only perform a read task, given an index of a
                document to find.  Then it should return that document.
        
                :param index: An integer describing the index of the document to find
        
                :return document: The document that was just found 
                """
                
                # A silly example
                document = self.client.read(Index=index)
        
                return document
                ```

5. Document your module!
    * create a `README.md` with any special information for your module, and also be sure to include plenty of in-line documentation.

6. Submit a Pull Request with your finished module!
