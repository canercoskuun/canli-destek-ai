from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


pdf_paths = [
    "cloudera-director.pdf",
    "cdpessentials-191031-student-slides.pdf",
    "cdppvc-data-services-overview.pdf",
    "cm-concepts.pdf",
    "dw-openshift-environments.pdf",
]
docs = [PyPDFLoader(pdf_path).load() for pdf_path in pdf_paths]
docs_list = [item for sublist in docs for item in sublist]

# Chunk ve vektör mağazası
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs_list)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="chroma_db"
)
retriever = vectorstore.as_retriever()