from main import mcp

@mcp.tool()
def ask_rag(question: str) -> dict:
    from graph import graph
    """
    RAG graph'ını çağırır ve cevabı MCP istemcilerine döner.
    Çıktı:
    {
      "answer": str,
      "sources_text": str  # boş olabilir
    }
    """
    result = graph.invoke({"question": question})

    answer = result.get("answer")
    sources_text = (result.get("sources_text")).strip()

    return {
        "answer": answer,
        "sources_text": sources_text,
    }





