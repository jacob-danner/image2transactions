from .opensearch.retrieve import OpenSearchRetriever
from langchain_openai import ChatOpenAI

from .opensearch.client import client, index_name

model = ChatOpenAI(model="gpt-4o")
retriever = OpenSearchRetriever(client=client, index_name=index_name)
