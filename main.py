"""
Main.py will house all of the benchmarking commands
"""

from mongo_db import BenchmarkMongo
from riak_db import BenchmarkRiak

import time
import string
import random

from numpy import array, average


class Benchmark():

    def __init__(self, db):

        self.entry_length = 10
        self.number_of_trials = 100
        self.write_times = []
        self.read_times = []

        self.collection = 'test'
        self.sorting_index = 'ID'

        registered_dbs = {
            'riak': BenchmarkRiak(),
            'mongo': BenchmarkMongo(),
        }

        self.database = registered_dbs.get(db)

        if not self.database:
            print 'Not a valid db!'

    def random_entry(self, entry_type='string'):

        entry = ''

        if entry_type == 'string':

            selection = string.ascii_letters

        else:

            selection = string.digits

        for x in range(self.entry_length):

            entry += random.choice(selection)

        return entry

    def run(self):

        for index in range(self.number_of_trials):

            info = self.random_entry(entry_type='string')
            item_number = self.random_entry(entry_type='number')

            entry = {self.sorting_index: index,
                     'Number': item_number,
                     'Info': info}

            if not self.writes(entry):
                print 'WRITE ERROR'

            if not self.reads():
                print 'WRITE ERROR'

        self.compile_data()

    def writes(self, entry):

        write_start_time = time.time()

        self.database.write(self.collection, self.sorting_index, entry)

        write_stop_time = time.time()

        write_time = write_stop_time - write_start_time

        self.write_times.append(write_time)

        return True

    def reads(self):

        read_start_time = time.time()

        self.database.read(self.collection, self.sorting_index)

        read_stop_time = time.time()

        read_time = read_stop_time - read_start_time

        self.read_times.append(read_time)

        return True

    def compile_data(self):

        self.write_times = array(self.write_times)
        self.read_times = array(self.read_times)

        write_avg = average(self.write_times)
        print write_avg

        read_avg = average(self.read_times)
        print read_avg

if __name__ == '__main__':

    foo = Benchmark('riak')

    foo.run()

