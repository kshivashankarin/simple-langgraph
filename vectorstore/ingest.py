import os

from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "company-docs"
)


def read_documents():

    documents = []

    documents_folder = "documents"

    for filename in os.listdir(documents_folder):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                documents_folder,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename
                    }
                )
            )

    return documents


def create_pinecone_index():

    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    existing_indexes = [
        index["name"]
        for index in pc.list_indexes()
    ]

    if PINECONE_INDEX_NAME not in existing_indexes:

        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print(
            f"Created index: {PINECONE_INDEX_NAME}"
        )

    else:

        print(
            f"Index already exists: {PINECONE_INDEX_NAME}"
        )


def ingest_documents():

    create_pinecone_index()

    documents = read_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    print(
        "Documents uploaded successfully."
    )


if __name__ == "__main__":

    ingest_documents()
