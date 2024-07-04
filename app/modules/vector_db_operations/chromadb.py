from app.utils.constants import (OPENAI_KEY,EMBEDDING_MODEL,
                                 LLM_MODEL,LOADER,
                                 SPLITTER,CHUNK_SIZE,
                                 CHUNK_OVERLAP,TEMPERATURE,
                                 )
from app.modules.vector_db_operations.base import BaseVectorDB
from app.modules.vector_db_operations.prompt_templates import QA_PROMPT,CONTEXTUALIZE_Q_PROMPT
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from app.modules.langchain_loaders.file_loaders import Loaders
from app.modules.langchain_splitter.text_splitters import Splitters
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStore
from langchain.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import warnings
warnings.filterwarnings("ignore")

class ChromaDb(BaseVectorDB):
    embedding = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMPERATURE, api_key=OPENAI_KEY)
    reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    reranker = CrossEncoderReranker(model=reranker_model,top_n=3)
    store = {}
    def __init__(self,collection_name):
        self.client = Chroma(embedding_function=self.embedding,
                            collection_name=collection_name,
                            persist_directory="chroma"
                            )
        
    def add_documents(self,data_path,collection_name) -> bool:
        if data_path.split(".")[-1] in ['pdf','txt']:
            docs = Loaders(LOADER).load(data_path)
        else:
            docs = Loaders().load(url_path=data_path)
        docs_splits = Splitters(SPLITTER).splits(
            docs,
            CHUNK_SIZE,
            CHUNK_OVERLAP
        )
        self.client.from_documents(documents=docs_splits, 
                                   embedding=self.embedding,
                                   collection_name=collection_name,
                                   persist_directory="chroma")
        return True
    
    def add_texts(self,text,collection_name) -> bool:
        self.client.from_texts(
            texts=[text],
            embedding=self.embedding,
            collection_name=collection_name,
            persist_directory="chroma"
        )
        return True
    
    def get_total_vector_count(self) -> int :
        return len(self.client.get()['documents'])
    
    def get_retriever(self,collection_name) -> VectorStore:
        return self.client.as_retriever(
            collection_name = collection_name,
            search_kwargs = {"k":3}
        )
    
    def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def retrieve_data_with_chat_history(self,retriever,query,sid):
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, CONTEXTUALIZE_Q_PROMPT
        )
        question_answer_chain = create_stuff_documents_chain(self.llm, QA_PROMPT)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        print("store",self.store)
        return conversational_rag_chain.invoke(
            {"input": query},
            config={
                "configurable": {"session_id": str(sid)}
            },
        )["answer"]
        
    def delete_collection(self) -> bool:
        self.client.delete_collection()
        return True
