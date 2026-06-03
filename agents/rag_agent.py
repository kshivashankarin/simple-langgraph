import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


def retrieve_relevant_doc_from_rag(state):

   question = state.get("standalone_question", state["user_question"])

   embeddings = OpenAIEmbeddings(
       model="text-embedding-3-small"
   )

   vectorstore = PineconeVectorStore(
       index_name=INDEX_NAME,
       embedding=embeddings
   )

   docs = vectorstore.similarity_search(
       question,
       k=3
   )

   content = "\n\n".join(
       [doc.page_content for doc in docs]
   )

   return {
       "retrieved_docs": content
   }
