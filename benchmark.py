"""
Becnhmark.py will house the parent class for all DB's to be benchmarked.
Each new DB will have a new class that inherits from this parent.
"""


class BenchmarkDatabase():

    def __init__(self):

        pass

    def setup(self):

        pass

    def write(self, collection, index, data):

        pass

    def read(self, collection, index):

        pass