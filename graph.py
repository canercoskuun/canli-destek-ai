from state import State
from langchain_core.output_parsers import StrOutputParser
from generation import llm, prompt
from ingestion import retriever
from typing import Dict,Any
from langgraph.graph import StateGraph, START, END
from typing import List
from langchain_core.documents import Document
from retrieval_grader import retrieval_grader
from langchain_core.runnables import RunnablePassthrough




# Grader ile doküman filtreleme
def filter_relevant_docs(question: str, documents: List[Document]) -> List[Document]:
    filtered = []
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        if score.binary_score.strip().lower() == "yes":
            filtered.append(d)
    return filtered



def pretty_sources(sources: List[Document]) -> str:
    seen = set()
    out = []
    for d in sources:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", None)
        key = (src, page)
        if key in seen:
            continue
        seen.add(key)
        out.append(f"- {src}" + (f" (p.{page})" if page is not None else ""))
    return "\n".join(out)



def retrieve_node(state: State) -> Dict[str, Any]:
    docs = retriever.invoke(state["question"])
    return {"documents": docs}

def grade_node(state: State) -> Dict[str, Any]:
    q = state["question"]
    docs = state.get("documents", [])
    relevant = filter_relevant_docs(q, docs)
    return {"documents": relevant}

def generate_node(state: State) -> Dict[str, Any]:
    q = state["question"]
    docs = state.get("documents", [])
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    answer = chain.invoke({"context": docs, "question": q})
    return {"answer": answer}

def not_relevant_node(state: State) -> Dict[str, Any]:
    return {"answer": "Ben sadece bana verilen ilgili dökümanlardaki sorulara cevap verebilecek bir chatbotum.Anlayışınız için teşekkürler.",
            "sources_text": ""}

def show_sources_node(state: State) -> Dict[str, Any]:
    docs = state.get("documents", [])
    sources = pretty_sources(docs)
    return {"sources_text": sources}

def route_after_grade(state: State) -> str:
    # İlgili doküman yoksa 'not_relevant', varsa 'generate'
    docs = state.get("documents", [])
    return "generate" if docs else "not_relevant"


builder = StateGraph(State)
builder.add_node("retrieve", retrieve_node)
builder.add_node("grade", grade_node)
builder.add_node("generate", generate_node)
builder.add_node("not_relevant", not_relevant_node)
builder.add_node("show_sources", show_sources_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")

builder.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "generate": "generate",
        "not_relevant": "not_relevant",
    },
)

builder.add_edge("generate", "show_sources")
builder.add_edge("show_sources", END)
builder.add_edge("not_relevant", END)

graph = builder.compile()

#graph.get_graph().draw_mermaid_png(output_file_path="graph.png")