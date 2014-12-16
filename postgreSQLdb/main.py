"""
DB Benchmarking Application
===========================

Mongo_db.py

This file handles all interactions with MongoDB during the benchmarking
process.

"""

import psycopg2
import os
import random

from local import *
from benchmark_template import BenchmarkDatabase


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection, setup=False, trials=0):

        if setup:
            self.setup(collection)

        self.trials = trials

        self.connections = {}
        self.cursors = []

    def setup(self, collection):
        """ This function will set up the connection with the DB.  The options
        used here are all configured in the config file.

        :param collection: The collection that all benchmark writes will happen
                    with

        """
        # #TODO - fix how the collection is used here

        lock_file = 'sql_{node}.lock'
        dir = 'postgreSQLdb'
        file_list = os.listdir(dir)

        for node in range(1, NUMBER_OF_NODES + 1):

            current_host = POSTGRESQL_NODES[
                'POSTGRESQL_{node}'.format(node=node)
            ]

            current_conn = psycopg2.connect(
                host=current_host,
                port=POSTGRESQL_PORT,
                user=POSTGRESQL_USER,
                password=POSTGRESQL_PASSWORD,
                dbname=collection,
            )

            self.connections[node] = current_conn

            current_cursor = self.connections[node].cursor()

            self.cursors[node] = current_cursor

            if lock_file in file_list:

                delete = 'DROP TABLE {table} cascade'.format(table=collection)

                self.cursors[node].execute(delete)

            else:

                current_lock = lock_file.format(node=node)

                with open('{dir}/{lock}'.format(lock=current_lock, dir=dir,), 'w+'):
                    pass

            create_table = 'CREATE TABLE test ' \
                           '({index}, {number}, {info});'.\
                format(
                    index='Index int',
                    number='Number int',
                    info='Info text',
                )

            self.cursors[node].execute(create_table)

            self.commit(node)

    def write(self, data):
        """ The function handles all writes with MongoDB.  It takes a single
        parameter (a dict of sample data) and then writes it to the DB.

        :param data: An incoming dict that will be written to the DB

        """

        node = random.randrange(0, stop=NUMBER_OF_NODES + 1)

        insert = 'INSERT INTO test (Index, Number, Info) VALUES ({Index}, ' \
                 '{Number}, {Info!r});'.format(**data)

        self.cur.execute(insert)

        self.commit(node)


    def read(self, index):
        """ This function handles all reads from MongoDB.  It takes a single
        parameter (index) which determines which record to retrieve from the DB.

        :param index: The index of the record to be retrieved from the DB

        :return read_entry: the entry retrieved from the DB

        """

        select = 'SELECT * from test WHERE Index = {index};'.format(index=index)

        self.cur.execute(select)
        return self.cur.fetchone()
    def node_select(self, trial):
        """

        :param trial:
        :return:
        """

        node = 1

        for n in range(1, NUMBER_OF_NODES + 1):

            split = self.split_points.get(n)

            if split and trial <= split:

                    node = n

        return node

    def commit(self, node):
        """ Commits the current transaction.  This function is ONLY USED FOR
        SQL-TYPE DATABASES.

        :return:
        """

        self.cursors[node].execute('commit;')

        # query = {
        #     'Index': index
        # }
        #
        # read_entry = self.collection.find_one(query)
        #
        # return read_entry
