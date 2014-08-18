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
        """ The init method is passed a single parameter upon initialization in
        order to define which database should be benchmarked.  Other important
        values are defined here, such as the entry length and the number of
        trials to execute.

        :param db: The desired db to be benchmarked
        """

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

        # A simple check to see if the desired database is registered
        if self.database:

            self.database.setup(self.collection, self.sorting_index)

        else:

            print 'Not a valid db!'

    def random_entry(self, entry_type='string'):
        """ This function generates a random string or random number depending on
        the arguments passed in.  The string is generated from all ascii letters
        and the number is generated from numbers 0-9.

        :param entry_type: the specified type of random entry, either 'string'
                            or 'number'
        :return: the random string or number that was just generated
        """

        entry = ''

        if entry_type == 'string':

            selection = string.ascii_letters

        else:

            selection = string.digits

        for x in range(self.entry_length):

            entry += random.choice(selection)

        return entry

    def run(self):
        """ This function will keep track of and call the read/ write functions
        for benchmarking.  For each iteration, a new DB entry will be created,
        written to the DB,  and then read back from it.

        """

        for index in range(self.number_of_trials):

            item_number = self.random_entry(entry_type='number')
            info = self.random_entry(entry_type='string')

            entry = {
                'Index': index,
                'Number': item_number,
                'Info': info
            }

            if not self.writes(entry):
                print 'WRITE ERROR'

            if not self.reads(index):
                print 'WRITE ERROR'

        self.compile_data()

    def writes(self, entry):
        """ This function handles all DB write commands, and times that action
        as well.  It takes a single parameter ('entry'), which is the data to be
        written to the DB.

        :param entry: The entry to be recorded to the DB
        :return: True, if all operations successfully completed
        """

        write_start_time = time.time()

        self.database.write(entry)

        write_stop_time = time.time()

        write_time = write_stop_time - write_start_time

        self.write_times.append(write_time)

        return True

    def reads(self, index):
        """ This function handles all DB read commands, and times that action as
        well.  It takes a single parameter, which is the index of an entry to
        retrieve from the DB.

        :param index: The index of the item to be retrieved from the DB
        :return: True, if all operations successfully completed
        """

        read_start_time = time.time()

        self.database.read(index)

        read_stop_time = time.time()

        read_time = read_stop_time - read_start_time

        self.read_times.append(read_time)

        return True

    def compile_data(self):
        """ This function takes all the data collected from the trials (read and
        write times) and then calculates some important statistics about said
        data.

        :return data: The compiled results from the statistical analysis of the
                        trial data
        """

        results = {}

        self.write_times = array(self.write_times)
        self.read_times = array(self.read_times)

        write_avg = average(self.write_times)
        print write_avg

        read_avg = average(self.read_times)
        print read_avg

        return results

if __name__ == '__main__':

    foo = Benchmark('mongo')

    foo.run()