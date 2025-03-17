from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_qdrant import RetrievalMode, QdrantVectorStore

from qdrant.bge_sparse_embeddings import BGEM3SparseEmbeddings

llm = OllamaLLM(model="gemma3:12b-it-q8_0", temperature=0)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3", model_kwargs={"device": "mps"}
)
sparse_embeddings = BGEM3SparseEmbeddings()
knowledge_base = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    sparse_embedding=sparse_embeddings,
    url=f"http://localhost:6333",
    prefer_grpc=True,
    collection_name="incidents",
    retrieval_mode=RetrievalMode.HYBRID,
)
reranker = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")


def retrieve_and_analyze_incident(incident_description):
    base_retriever = knowledge_base.as_retriever(search_kwargs={"k": 10})
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=CrossEncoderReranker(model=reranker, top_n=4),
        base_retriever=base_retriever,
    )

    system_prompt = """
        You are an e-commerce incident analysis assistant. You'll analyze the provided incident description and use the retrieved similar past incidents to determine the most probable root cause analysis (RCA) and resolution.
        
        The retrieved context contains similar past incidents with their descriptions, actions taken, resolutions, and root cause analyses. Use this information to make an informed assessment of the current incident.
        
        Guidelines:
        - Only use the information from the retrieved similar incidents
        - If the root cause and resolution cannot be determined based on the provided context, indicate that you cannot determine
        - Do not invent or assume information not present in the context
        - Focus on patterns and similarities between current incident and past incidents
        
        Retrieved similar incidents:
        {context}
        
        Return your analysis in the following JSON format only:
        {{
          "resolution": "The most probable resolution based on similar incidents, or 'CANNOT_DETERMINE' if unsure",
          "rca": "The most probable root cause analysis based on similar incidents, or 'CANNOT_DETERMINE' if unsure"
        }}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "New incident description: {input}"),
        ]
    )

    incident_analysis_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(compression_retriever, incident_analysis_chain)
    response = rag_chain.invoke(
        {"input": incident_description},
        config={"callbacks": [ConsoleCallbackHandler()]},
    )
    return response.get("answer")


print(
    retrieve_and_analyze_incident(
        "The website is down and customers are unable to place orders."
    )
)

print(
    retrieve_and_analyze_incident(
        "Price mismatch between the product page and the checkout page"
    )
)
