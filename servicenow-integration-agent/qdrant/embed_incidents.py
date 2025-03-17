import uuid

import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import RetrievalMode, QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from bge_sparse_embeddings import BGEM3SparseEmbeddings


def main():
    response = requests.get("http://localhost:8000/incidents")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch incidents: {response.status_code}")
    incidents = response.json()

    print(f"Processing {len(incidents)} incidents...")

    documents = []
    for incident in incidents:
        content = f"Incident Description: {incident.get('description', '')}\n\n"
        content += f"Actions Taken: {incident.get('actions_taken', '')}\n\n"
        content += f"Root Cause Analysis: {incident.get('rca', '')}\n\n"
        content += f"Resolution: {incident.get('resolution', '')}"

        doc = Document(
            page_content=content,
            metadata={
                "incident_id": incident.get("id", str(uuid.uuid4())),
            },
        )
        documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=1536,
        chunk_overlap=256,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} incidents")

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3", model_kwargs={"device": "mps"}
    )

    sparse_embeddings = BGEM3SparseEmbeddings()

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        url=f"http://localhost:6333",
        prefer_grpc=True,
        collection_name="incidents",
        force_recreate=True,
        retrieval_mode=RetrievalMode.HYBRID,
    )

    print("Embedding completed and stored in Qdrant.")


if __name__ == "__main__":
    main()
