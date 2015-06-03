"""
DB Benchmarking Application
===========================

Mongo_db.py

This file handles all interactions with MongoDB during the benchmarking
process.

"""

from pymongo import MongoClient

from local import *
from benchmark_template import BenchmarkDatabase


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection, setup=False, trials=0):

        self.trials = trials

        if setup:
            self.setup(collection)

        self.collection = None

    def setup(self, collection):
        """ This function will set up the connection with the DB.  The options
        used here are all configured in the config file.

        :param collection: The collection that all benchmark writes will happen
                    with

        """
        #TODO - fix how the collection is used here

        client = MongoClient(host=MONGO_PRIMARY, port=MONGO_PORT)

        db = client.test

        self.collection = db.test_collection

        self.collection.ensure_index("Index")

    def write(self, data):
        """ The function handles all writes with MongoDB.  It takes a single
        parameter (a dict of sample data) and then writes it to the DB.

        :param data: An incoming dict that will be written to the DB

        """

        self.collection.insert(data)

    def read(self, index):
        """ This function handles all reads from MongoDB.  It takes a single
        parameter (index) which determines which record to retrieve from the DB.

        :param index: The index of the record to be retrieved from the DB

        :return read_entry: the entry retrieved from the DB

        """

        query = {
            'Index': index
        }

        read_entry = self.collection.find_one(query)

        return read_entry