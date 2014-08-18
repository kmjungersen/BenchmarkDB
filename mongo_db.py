__author__ = 'kurtisjungersen'

from benchmark_template import BenchmarkDatabase
from pymongo import MongoClient

from load_settings import LocalSettings

CONFIG = LocalSettings()


class BenchmarkMongo():

    def __init__(self, setup=False):

        if setup:
            self.setup('test', 'ID')

        self.client = ''
        self.db = ''

    def setup(self, collection, sorting_index):

        self.client = MongoClient(host=CONFIG.vagrant_1, port=CONFIG.mongo_port)

        self.db = self.client.mydb

        self.collection = self.db.testData

    def write(self, data):

        self.collection.insert(data)

    def read(self, index):

        query = {
            'Index': index
        }

        print self.collection.find_one(query)


if __name__ == '__main__':

    foo = BenchmarkMongo()