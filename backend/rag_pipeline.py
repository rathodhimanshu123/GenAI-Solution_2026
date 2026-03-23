import os
import logging
from typing import List, Tuple
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

logger = logging.getLogger(__name__)

FAISS_PATH = os.path.join(os.path.dirname(__file__), "data", "faiss_index")

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "bn": "Bengali",
    "te": "Telugu",
    "kn": "Kannada",
    "mr": "Marathi",
    "gu": "Gujarati",
}

class RAGPipeline:
    def __init__(self):
        self._initialized = False
        self.vectorstore = None
        self.embeddings = None
        self.llm = None
        self.api_key = None

    def initialize(self):
        """Initialize the RAG pipeline."""
        if self._initialized:
            return

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment")
            return

        try:
            # Initialize Embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=self.api_key
            )

            # Initialize LLM
            self.llm = ChatGoogleGenerativeAI(
                model="models/gemini-flash-latest",
                google_api_key=self.api_key,
                temperature=0.3,
            )

            # Load or Create Vector Store
            if os.path.exists(FAISS_PATH):
                self.vectorstore = FAISS.load_local(
                    str(FAISS_PATH), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Loaded existing FAISS index")
            else:
                # Create empty index if no documents yet
                texts = ["VedaVerse is a project for Indian Knowledge Systems."]
                self.vectorstore = FAISS.from_texts(texts, self.embeddings)
                os.makedirs(os.path.dirname(FAISS_PATH), exist_ok=True)
                self.vectorstore.save_local(str(FAISS_PATH))
                logger.info("Created new FAISS index")

            self._initialized = True
            logger.info("RAG pipeline initialized successfully")

        except Exception as e:
            logger.error(f"RAG initialization failed: {e}")
            self._initialized = False

    def query(self, question: str, target_language: str = "en", k: int = 4) -> Tuple[str, List[dict]]:
        """Run RAG query. Returns (answer, sources)."""
        if not self._initialized:
            return self._mock_response(question), []

        try:
            # 1. Retrieve relevant documents
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
            relevant_docs = retriever.invoke(question)

            # 2. Extract language name
            lang_name = LANGUAGE_NAMES.get(target_language, "English")

            # 3. Construct Context
            context = "\n---\n".join([doc.page_content for doc in relevant_docs])

            # 4. Construct Prompt (Multilingual Instruction)
            prompt = f"""You are VedaVerse, a knowledgeable assistant specializing in Indian Knowledge Systems (IKS).
Answer the user's question using ONLY the provided context from ancient Indian texts.

IMPORTANT: You must provide your answer in {lang_name}. 
If the question is in another language, translate it internally and then answer in {lang_name}.
If the context doesn't contain the answer, say so in {lang_name}.

Context:
{context}

Question: {question}

Answer in {lang_name}:"""

            # 5. Generate Response
            response = self.llm.invoke(prompt)
            answer = response.content

            # 6. Format Sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "title": doc.metadata.get("source", "Ancient Text"),
                    "category": doc.metadata.get("category", "General"),
                    "excerpt": doc.page_content[:200] + "...",
                    "page": doc.metadata.get("page"),
                })

            return answer, sources

        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            if not self._initialized:
                return self._mock_response(question), []
            raise e

    def _mock_response(self, question: str) -> str:
        return "I am running in mock mode. Please check your API key to get real AI answers."

rag_pipeline = RAGPipeline()
