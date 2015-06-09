"""

"""
from __future__ import absolute_import

from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from cassandra.cqlengine import columns, models

from benchmark_template import BenchmarkDatabase

from .local import *


class Benchmark(BenchmarkDatabase):

    def __init__(self, collection, trials=0, setup=False):

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """

        :param collection:
        :return:
        """

        connection.setup([CASSANDRA_1], collection)

        management.create_keyspace(
            collection,
            replication_factor=1,
            strategy_class='SimpleStrategy',
        )

        TestModel.__keyspace__ = collection
        management.sync_table(TestModel)

    def write(self, data):
        """

        :param data:
        :return:
        """
        TestModel.create(**data).save()

    def read(self, index):
        """

        :return:
        """

        # document = TestModel.get(
        #     source=source,
        #     docID=docID,
        # )

        document = TestModel.get(
            Index=index
        )

        return dict(document)


class TestModel(models.Model):
    Index = columns.Integer(primary_key=True)
    Number = columns.BigInt()
    Info = columns.Text()


class DocumentModel(models.Model):
    __table_name__ = 'documents'

    # Raw
    source = columns.Text(primary_key=True, partition_key=True)
    docID = columns.Text(primary_key=True, index=True, clustering_order='ASC')

    doc = columns.Bytes()
    filetype = columns.Text()
    timestamps = columns.Map(columns.Text, columns.Text)

    # Normalized
    uris = columns.Text()
    title = columns.Text()
    contributors = columns.Text()
    providerUpdatedDateTime = columns.DateTime()

    description = columns.Text()
    freeToRead = columns.Text()
    languages = columns.List(columns.Text())
    licenses = columns.Text()
    publisher = columns.Text()
    subjects = columns.List(columns.Text())
    tags = columns.List(columns.Text())
    sponsorships = columns.Text()
    version = columns.Text()
    otherProperties = columns.Text()
    shareProperties = columns.Text()

    # Additional metadata
    versions = columns.List(columns.UUID)
