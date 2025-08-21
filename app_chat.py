import streamlit as st
from tools.ask import ask_rag



# ----- HEADER -----
st.title("💬Cloudera Support Asistant")
st.caption("🚀 A Streamlit chatbot powered by Cloudera Documents")

# ----- SESSION INIT -----
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant",
         "content": "Hello! I’m the Cloudera Support Assistant. How can I assist you with your data platform needs today?"
         }]

# ----- MESSAGE DISPLAY -----
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# ----- USER INPUT -----
if prompt := st.chat_input("Write your question..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
      with st.spinner("🤖 Bot is thinking..."):
        response = ask_rag(prompt)
        answer = response.get("answer", "Sorry, I couldn't find an answer to your question.")
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
    except Exception as e:
        answer = f"An error occurred: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write("Bir hata oluştu. Lütfen tekrar deneyin.")

