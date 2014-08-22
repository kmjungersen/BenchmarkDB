"""
DB Benchmarking Application
===========================

Benchmark.py

This file houses the basic template for a new module's `main.py`.  This template
** MUST BE FOLLOWED ** in order for the benchmarking application to function
properly.  Read the docstrings carefully!

NOTE: Any variable settings needed for this module should be housed in a
`local.py` file in the module directory.  Then import those settings like so:

    from local import *

Now any settings defined there can be accessed from the `Benchmark` class.

"""


class BenchmarkDatabase():

    def __init__(self, collection, setup=False):
        """ `__init__()` is the entry point of the module, and is where the
        module is set up and prepared for benchmarking.  This class is
        initialized in `main.py` of the main project directory, and is always
        called with the optional parameter `setup=True`.  It defaults to `False`
        for the sole reason of building tests.

        :param collection: The collection of the DB which all reads and
                    writes will occur with
        :param setup: A Bool to determine whether or not `setup()` should be
                    called upon initialization or not
        """

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """ This function handles all of the setup operations for the database
        reads and writes.  It is typically called from `__init__()`, although
        not necessarily in the case of tests.  It is crucial that this function
        sets up the client-database connection for use in other functions of this
        class.  A `local.py` file should exist in the module directory and should
        include the IP addresses and ports needed to connect to the DB.

        :param collection: The collec
        :return:
        """
        pass

    def write(self, data):

        pass

    def read(self, index):

        pass