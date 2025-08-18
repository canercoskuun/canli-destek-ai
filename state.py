from typing import TypedDict,List
from langchain_core.documents import Document

class State(TypedDict):
    question: str
    documents: List[Document]
    answer: str
    sources_text: str
