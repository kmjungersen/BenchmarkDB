"""
DB Benchmarking Application
===========================

Riak_db.py

This file handle all interactions with RiakDB during the benchmarking process.

"""

import riak

from load_settings import LocalSettings
from benchmark_template import BenchmarkDatabase

CONFIG = LocalSettings()


class BenchmarkRiak(BenchmarkDatabase):

    def __init__(self, setup=False):

        if setup:
            self.setup('test')

    def setup(self, collection):
        """ `Setup()` handles all the necessary setup information for Riak.  It
        creates an instance of a Riak Client and defines the collection to use
        for reads and writes.

        :param collection:
        :return:
        """
        port = CONFIG.riak_port

        riak_servers = [
            CONFIG.riak_1,
            CONFIG.riak_2,
            CONFIG.riak_3,
        ]

        riak_nodes = []

        for server in riak_servers:

            riak_nodes.append({'host': str(server), 'http_port': port})

        self.client = riak.RiakClient(nodes=riak_nodes)

        self.bucket = self.client.bucket(collection)

    def write(self, data):

        entry = self.bucket.new('ID', data=data)

        entry.store()

    def read(self, index):

        read_entry = self.bucket.get('ID').data

        # print read_entry


if __name__ == '__main__':

    foo = BenchmarkRiak()