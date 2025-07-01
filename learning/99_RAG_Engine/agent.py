from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

load_dotenv()

ask_vertex_retrieval = VertexAiRagRetrieval(
    name="retrieve_rag_documentation",
    description=(
        "Use this tool to retrieve documentation and reference materials for"
        " the question from the RAG corpus,"
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus=os.environ.get("RAG_CORPUS"),
        )
    ],
    similarity_top_k=1,
    vector_distance_threshold=0.6,
)

root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    instruction=(
        "You are an AI assistant with access to specialized corpus of"
        " documents. Your role is to provide accurate and concise answers to"
        " questions based on documents that are retrievable using"
        " ask_vertex_retrieval."
    ),
    tools=[ask_vertex_retrieval],
)