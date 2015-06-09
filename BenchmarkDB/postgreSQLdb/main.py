"""
DB Benchmarking Application
===========================

Mongo_db.py

This file handles all interactions with MongoDB during the benchmarking
process.

"""
from __future__ import absolute_import

import os

import psycopg2
from .local import *

from benchmark_template import BenchmarkDatabase
from six.moves import range


class Benchmark():

    def __init__(self, collection, setup=False, trials=0):

        self.trials = trials
        self.split_points = {}

        self.connections = {}
        self.cursors = {}

        self.insert_statement = """INSERT INTO test (Index, Number, Info)
                                       VALUES (
                                           {Index},
                                           {Number},
                                           {Info!r}
                                       );"""

        self.delete_statement = 'DROP TABLE {table} cascade'

        self.create_statement = """CREATE TABLE test (
                                       Index   INTEGER PRIMARY KEY,
                                       Number  BIGINT,
                                       Info    TEXT
                                   );"""

        self.select_statement = 'SELECT * from test WHERE Index = {index};'

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """ This function will set up the connection with the DB.  The options
        used here are all configured in the config file.

        :param collection: The collection that all benchmark writes will happen
                    with

        """
        # #TODO - fix how the collection is used here

        import ipdb
        # ipdb.set_trace()

        lock_file = '.sql_{node}.lock'
        dir = 'postgreSQLdb'
        file_list = os.listdir(dir)

        split_number = self.trials / NUMBER_OF_NODES

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

            current_lock = lock_file.format(node=node)

            if current_lock in file_list:

                delete = self.delete_statement.format(table=collection)

                self.cursors[node].execute(delete)

                self.commit(node)

            else:

                with open('{dir}/{lock}'.format(lock=current_lock, dir=dir,), 'w+'):
                    pass

            # create_table = self.create_statement.format(
            #     index='Index int',
            #     number='Number int',
            #     info='Info text',
            # )

            self.cursors[node].execute(self.create_statement)

            self.commit(node)

            self.split_points[node] = split_number * node

    def write(self, data):
        """ The function handles all writes with MongoDB.  It takes a single
        parameter (a dict of sample data) and then writes it to the DB.

        :param data: An incoming dict that will be written to the DB

        """

        trial = data['Index']
        node = self.node_select(trial)

        insert = self.insert_statement.format(**data)

        self.cursors[node].execute(insert)

        self.commit(node)

    def read(self, index):
        """ This function handles all reads from MongoDB.  It takes a single
        parameter (index) which determines which record to retrieve from the DB.

        :param index: The index of the record to be retrieved from the DB

        :return read_entry: the entry retrieved from the DB

        """

        node = self.node_select(index)

        select = self.select_statement.format(index=index)

        self.cursors[node].execute(select)

        return self.cursors[node].fetchone()

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