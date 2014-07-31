import riak

from load_settings import LocalSettings
from benchmark import BenchmarkDatabase

CONFIG = LocalSettings()

class BenchmarkRiak(BenchmarkDatabase):

    def __init__(self):
        self.client = ''

        self.customer = {
            'customer_id': 1,
            'name': "John Smith",
            'address': "123 Main Street",
            'city': "Columbus",
            'state': "Ohio",
            'zip': "43210",
            'phone': "+1-614-555-5555",
            'created_date': "2013-10-01 14:30:26"
        }

        self.orders = [
        {
            'order_id': 1,
            'customer_id': 1,
            'salesperson_id': 9000,
            'items': [
                {
                    'item_id': "TCV37GIT4NJ",
                    'title': "USB 3.0 Coffee Warmer",
                    'price': 15.99
                },
                {
                    'item_id': "PEG10BBF2PP",
                    'title': "eTablet Pro, 24GB, Grey",
                    'price': 399.99
                }
            ],
            'total': 415.98,
            'order_date': "2013-10-01 14:42:26"
        },
        {
            'order_id': 2,
            'customer_id': 1,
            'salesperson_id': 9001,
            'items': [
                {
                    'item_id': "OAX19XWN0QP",
                    'title': "GoSlo Digital Camera",
                    'price': 359.99
                }
            ],
            'total': 359.99,
            'order_date': "2013-10-15 16:43:16"
        },
        {
            'order_id': 3,
            'customer_id': 1,
            'salesperson_id': 9000,
            'items': [
                {
                    'item_id': "WYK12EPU5EZ",
                    'title': "Call of Battle: Goats - Gamesphere 4",
                    'price': 69.99
                },
                {
                    'item_id': "TJB84HAA8OA",
                    'title': "Bricko Building Blocks",
                    'price': 4.99
                }
            ],
            'total': 74.98,
            'order_date': "2013-11-03 17:45:28"
        }]

        self.order_summary = {
            'customer_id': 1,
            'summaries': [
                {
                    'order_id': 1,
                    'total': 415.98,
                    'order_date': "2013-10-01 14:42:26"
                },
                {
                    'order_id': 2,
                    'total': 359.99,
                    'order_date': "2013-10-15 16:43:16"
                },
                {
                    'order_id': 3,
                    'total': 74.98,
                    'order_date': "2013-11-03 17:45:28"
                }
            ]
        }



    def setup(self):

        riak_servers = [CONFIG.mongo_ip_1, CONFIG.mongo_ip_2, CONFIG.mongo_ip_3]

        riak_nodes = []

        for server in riak_servers:

            riak_nodes.append({'host': str(server), 'http_port': 8098})

        self.client = riak.RiakClient(nodes=[{'host': '192.168.33.11', 'http_port': 8098}])



    def write(self, data):

        self.customer_bucket = self.client.bucket('Customers')
        self.order_bucket = self.client.bucket('Orders')
        self.order_summary_bucket = self.client.bucket('OrderSummaries')

        cr = customer_bucket.new(str(self.customer['customer_id']),
                         data=self.customer)
        cr.store()

    def read(self, data):
        customer =
