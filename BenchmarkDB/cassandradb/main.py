"""
DB Benchmarking Application


"""

from BenchmarkDB.benchmark_template import BenchmarkDatabase

from BenchmarkDB.cassandradb.utils.util import documents


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection, setup=False, trials=0):

        self.cluster = None
        self.session = None
        #
        # self.create_statement = 'CREATE TABLE {keyspace}_table (id INT Index, BIGINT Number, TEXT Info)'
        #
        # self.select_statement = 'SELECT '

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """

        :param collection:
        :return:
        """

        # self.cluster = Cluster([
        #     CASSANDRA_1,
        #     ])
        #
        # self.session = self.cluster.connect()
        # self.session.set_keyspace(CASSANDRA_KEYSPACE)

    def write(self, data):
        """

        :param data:
        :return:
        """

        pass

    def read(self, index):
        """

        :param index:
        :return:
        """

        docs = documents('asu')

        return docs

    #TODO - make private
    def create_tables(self):
        """

        :return:
        """
        #
        # cmd = self.create_statement.format(
        #     kepspace=CASSANDRA_KEYSPACE,
        #     )
        #
        # self.session.execute(cmd)