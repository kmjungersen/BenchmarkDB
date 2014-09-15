"""
DB Benchmarking Application
===========================

Riak_db.py

This file handle all interactions with RiakDB during the benchmarking process.

"""

import riak

from local import *
from benchmark_template import BenchmarkDatabase


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection, setup=False):

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """ `Setup()` handles all the necessary setup information for Riak.  It
        creates an instance of a Riak Client and defines the collection to use
        for reads and writes.

        :param collection:
        :return:
        """

        port = RIAK_PORT

        riak_servers = [
            RIAK_1,
            RIAK_2,
            RIAK_3,
        ]

        riak_nodes = []

        for server in riak_servers:

            riak_nodes.append({'host': str(server), 'http_port': port})

        self.client = riak.RiakClient(nodes=riak_nodes, protocol='pbc', pb_port=10017)

        self.bucket = self.client.bucket(collection)

    def write(self, data):

        entry = self.bucket.new('ID', data=data)

        entry.store()

    def read(self, index):

        read_entry = self.bucket.get(str(index)).data

        return read_entry