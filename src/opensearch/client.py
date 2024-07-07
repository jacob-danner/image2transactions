from opensearchpy import OpenSearch

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)


def init_client() -> OpenSearch:
    host = 'localhost'
    port = 9200
    auth = ('admin', 'Image2Transaction$')

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
    )

    return client


client = init_client()
index_name = 'transactions'
