__author__ = 'kurtisjungersen'

from benchmark import BenchmarkDatabase
from PyMongo import MongoClient

from load_settings import LocalSettings

CONFIG = LocalSettings()


class BenchmarkMongo(BenchmarkDatabase):

    def __init__(self):

        self.client = ''
        self.db = ''
        self.collection = ''

        self.setup()

    def setup(self):

        self.client = MongoClient(host=CONFIG.vagrant_1, port=CONFIG.mongo_port)

        self.db = self.client.mydb

        self.collection = self.db.testData

    def write(self, collection, index, data):

        new_entry = {
            'index': index,
            'data': data,
        }

        self.collection.insert(new_entry)

    def read(self, collection, index):

        self.collection.find()

        return data