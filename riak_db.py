import riak

from load_settings import LocalSettings
from benchmark import BenchmarkDatabase

CONFIG = LocalSettings()

class BenchmarkRiak(BenchmarkDatabase):

    def __init__(self):

        self.setup()

    def setup(self):

        riak_servers = [
            CONFIG.vagrant_1,
            CONFIG.vagrant_2,
            CONFIG.vagrant_3,
        ]

        riak_nodes = []

        for server in riak_servers:

            riak_nodes.append({'host': str(server), 'http_port': 8098})

        print riak_nodes

        # foo_node = [{'host': '192.168.33.11', 'http_port': 8098}]

        self.client = riak.RiakClient(nodes=riak_nodes)

    def write(self, collection, index, data):

        bucket = self.client.bucket(collection)

        entry = bucket.new('ID', data=data)

        entry.store()

    def read(self, collection, index):

        bucket = self.client.bucket(collection)

        read_entry = bucket.get('ID').data

        # return True

if __name__ == '__main__':

    foo = BenchmarkRiak()