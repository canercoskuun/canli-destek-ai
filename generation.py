from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


model = os.getenv("GROQ_MODEL")
llm = ChatGroq(model=model)
# Prompt
message = """
You are a knowledgeable assistant for answering questions using the provided context.
Follow these rules strictly:
1. Use only the information from the context to answer.
2. Be concise, clear, and factual.
3. Do not add any extra information not found in the context.

Question:
{question}

Context:
{context}

Answer:
"""
prompt = ChatPromptTemplate.from_messages([("human", message)])
