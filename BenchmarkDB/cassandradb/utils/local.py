DEBUG = False

ELASTIC_TIMEOUT = 10
ELASTIC_INDEX = 'share_v2'
ELASTIC_URI = 'localhost:9200'

BROKER_URL = 'amqp://guest@localhost'

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

RECORD_HTTP_TRANSACTIONS = True

NORMALIZED_PROCESSING = ['cassandra', 'elasticsearch']
RAW_PROCESSING = ['cassandra']

SENTRY_DSN = None

USE_FLUENTD = False
FLUENTD_ARGS = {
    'tag': 'app.scrapi'
}


CASSANDRA_URI = ['192.168.59.104']
CASSANDRA_KEYSPACE = 'scrapi'

FRONTEND_KEYS = [
    u'description',
    u'contributors',
    u'tags',
    u'raw',
    u'title',
    u'id',
    u'source',
    u'dateUpdated'
]
