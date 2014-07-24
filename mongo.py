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


        pass

    def setup(self):

        self.client = MongoClient(host=CONFIG.mongo_ip, port=CONFIG.mongo_port)

        self.db = self.client.mydb

        self.collection = self.db.testData

        pass

    def write(self, data):

        pass

    def read(self, query):

        self.collection.find()

        return data