"""
DB Benchmarking Application
===========================

Benchmark.py

This file houses the basic template for a new module's `main.py`. This template
** MUST BE FOLLOWED ** in order for the benchmarking application to function
properly.  Read the docstrings carefully!

NOTE: Any variable settings needed for this module should be housed in a
`local.py` file in the module directory.  Then import those settings like so:

    from local import *

Now any settings defined there can be accessed from the `Benchmark` class.

"""

# This import will only work in the appropriate module
from local import *


class BenchmarkDatabase():

    def __init__(self, collection, setup=False, trials=0):
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

    def write(self, data):
        """ This function should only perform a write task, given a document
        to write to the database.

        :param data: a dictionary-type document that will be written to the db
        """

    def read(self, index):
        """ This function should only perform a read task, given an index of a
        document to find.  Then it should return that document.

        :param index: an integer describing the index of the document to find

        :return document: the document that was just pulled from the database
        """

        example_document = {
            'Index': index,
            'Number': 123456789,
            'Info': 'asdflkjh',
        }

        return example_document