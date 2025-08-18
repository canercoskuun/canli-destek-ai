from graph import graph



if __name__ == "__main__":
    while True:
        question = input("> ")
        if question.lower() == "q":
            print("Exit...")
            break

        result = graph.invoke({"question": question})
        print(result["answer"])

        src_text = (result.get("sources_text") or "").strip()
        if src_text:
            print("\n---\nSources:")
            print(src_text)
