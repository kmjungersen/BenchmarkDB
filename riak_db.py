import riak

from load_settings import LocalSettings
from benchmark_template import BenchmarkDatabase

CONFIG = LocalSettings()


class BenchmarkRiak(BenchmarkDatabase):

    def __init__(self, setup=False):

        if setup:
            self.setup('test')

    def setup(self, collection):

        port = CONFIG.riak_port

        riak_servers = [
            CONFIG.vagrant_1,
            CONFIG.vagrant_2,
            CONFIG.vagrant_3,
        ]

        riak_nodes = []

        for server in riak_servers:

            riak_nodes.append({'host': str(server), 'http_port': port})

        print riak_nodes

        # foo_node = [{'host': '192.168.33.11', 'http_port': 8098}]

        self.client = riak.RiakClient(nodes=riak_nodes)

        self.bucket = self.client.bucket(collection)


    def write(self, index, data):

        entry = self.bucket.new('ID', data=data)

        entry.store()

    def read(self, index):

        read_entry = self.bucket.get('ID').data

        # return True

if __name__ == '__main__':

    foo = BenchmarkRiak()