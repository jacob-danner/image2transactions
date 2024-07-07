from opensearchpy import OpenSearch
import uuid


def add_index(client: OpenSearch, index_name: str) -> None:
    client.indices.create(
        index_name,
        body={
            "settings": {"index": {"number_of_shards": 1}},
            "mappings": {
                "properties": {
                    "vendor": {"type": "text"},
                    "day": {"type": "text"},
                    "amount": {"type": "float"},
                    "from_account": {"type": "text"},
                }
            },
        },
    )


DataDict = dict[str, dict[str, str]]


def flatten_data(data: DataDict) -> dict[str, str]:
    flattened = [{"vendor": t_name, **t_values} for t_name, t_values in data.items()]

    return flattened


def add_documents(
    client: OpenSearch, index_name: str, all_data: list[DataDict]
) -> None:
    merged_data = {k: v for d in all_data for k, v in d.items()}
    documents = flatten_data(merged_data)

    for document in documents:
        client.index(
            index=index_name, body=document, id=str(uuid.uuid4()), refresh=True
        )
