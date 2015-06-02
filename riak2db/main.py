"""
DB Benchmarking Application
===========================

Riak_db.py

This file handle all interactions with RiakDB during the benchmarking process.

"""

import riak

from local import *
from benchmark_template import BenchmarkDatabase
from clint.textui import progress


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection=None, setup=False, trials=1000, flush=True):

        self.bucket = None

        if setup and collection:
            self.bucket = self.setup(collection)

            if flush:
                # pass
                self.flush_database()

    def setup(self, collection):
        """ `Setup()` handles all the necessary setup information for Riak.  It
        creates an instance of a Riak Client and defines the collection to use
        for reads and writes.

        :param collection:
        """

        port = RIAK_PORT

        riak_servers = [
            RIAK_1,
            RIAK_2,
            RIAK_3,
        ]

        riak_cluster = []

        for server in riak_servers:

            riak_cluster.append({
                'host': str(server),
                'pbc_port': port
            })

        client = riak.RiakClient(
            nodes=riak_cluster,
        )

        bucket = client.bucket(collection)

        if not self.bucket:

            self.bucket = bucket

        return bucket

    def flush_database(self):
        """ This function flushes the database entirely so that each benchmark
        is run with a clean database.
        """

        print 'flushing database....'

        if self.bucket:

            for keys in self.bucket.stream_keys():

                for key in keys:

                    self.bucket.delete(key)

        else:

            msg = 'Error! Riak client connection not established!'

            exit(msg)

    def write(self, data):
        """ This function defines a new bucket entry with the given data and
         then writes it to the Riak cluster.

         :param data: The data to be written to the db
         """

        entry = self.bucket.new(str(data['Index']), data=data)

        entry.store()

    def read(self, index):
        """ This function reads the last entry from Riak and then returns it
        to the primary application.

        :param index: An unused parameter that describes the most recent index

        :return read_entry: the entry that was just retrieved from Riak
        """

        read_entry = self.bucket.get(str(index)).data

        return read_entry