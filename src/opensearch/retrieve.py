from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from opensearchpy import OpenSearch


class OpenSearchRetriever(BaseRetriever):
    client: OpenSearch
    index_name: str

    def _get_relevant_documents(self, query: str) -> list[Document]:
        query_terms = query.split()
        should_clauses = [
            {"wildcard": {"vendor": {"value": f"*{term}*", "case_insensitive": True}}}
            for term in query_terms
        ]

        search_query = {"size": 10, "query": {"bool": {"should": should_clauses}}}

        response = self.client.search(index=self.index_name, body=search_query)

        documents = [
            Document(page_content=str(hit["_source"]))
            for hit in response["hits"]["hits"]
        ]

        return documents
