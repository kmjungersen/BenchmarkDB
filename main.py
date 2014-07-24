"""
Main.py will house all of the benchmarking commands
"""

from mongo import BenchmarkMongo as Mongo

import time
import string
import random


class Benchmark():

    def __init__(self):

        self.entry_length = 10

        pass

    def random_entry(self, type='string'):

        entry = ''

        if type == 'string':

            selection = string.ascii_letters

        else:

            selection = string.digits

        for x in range(self.entry_length):

            entry += random.choice(selection)

        return entry


