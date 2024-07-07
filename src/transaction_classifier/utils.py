from langchain.schema import Document
from ..models import CleanedTransaction


def format_context(docs: list[Document]):
    return "\n".join([d.page_content for d in docs])


def stringify_transaction(t: CleanedTransaction) -> str:
    return t.model_dump_json()


def runnable_log_to_file(
    label: str,
    to_return: any,
    content: str = None
) -> any:
    with open('logs.md', 'a') as logs:
        if content is not None:
            logs.write(f'{label}:\n{content}\n\n')
        else:
            logs.write(f'{label}\n\n')
    return to_return
