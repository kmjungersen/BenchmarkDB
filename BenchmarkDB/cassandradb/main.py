from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from cassandra.cqlengine import columns, models

from benchmark_template import BenchmarkDatabase

from local import CASSANDRA_1


class Benchmark(BenchmarkDatabase):

    def setup(self, collection):
        connection.setup(CASSANDRA_1, collection)
        management.create_keyspace(
            collection,
            replication_factor=1,
            strategy_class='SimpleStrategy'
        )
        DocumentModel.__keyspace__ = collection
        management.sync_table(DocumentModel)

    def read(self, (source, docID)):
        return DocumentModel.get(source=source, docID=docID)

    def write(self, data):
        DocumentModel.create(**data).save()


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
