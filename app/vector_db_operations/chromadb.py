from app.utils.constants import (
    OPENAI_KEY,
    EMBEDDING_MODEL,
    LLM_MODEL,
    LOADER,
    SPLITTER,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TEMPERATURE,
)
from app.vector_db_operations.base import BaseVectorDB
from app.vector_db_operations.prompt_templates import (
    QA_PROMPT,
    CONTEXTUALIZE_Q_PROMPT,
)
from app.chat_history.db import ChatHistory

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from app.utils.langchain_utils import Loaders
from app.utils.langchain_utils import Splitters
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

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
    # embedding = OpenAIEmbeddings()
    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMPERATURE, api_key=OPENAI_KEY)
    store = {}

    def __init__(self, collection_name):
        self.client = Chroma(
            embedding_function=self.embedding,
            collection_name=collection_name,
            persist_directory="chroma",
        )


    def add_documents(self, data_path, collection_name) -> bool:
        try:
            if data_path.split(".")[-1] in ["pdf", "txt"]:
                docs = Loaders(LOADER).load(data_path)
            else:
                docs = Loaders().load(url_path=data_path)
            docs_splits = Splitters(SPLITTER).splits(docs, CHUNK_SIZE, CHUNK_OVERLAP)
            self.client.from_documents(
                documents=docs_splits,
                embedding=self.embedding,
                collection_name=collection_name,
                persist_directory="chroma",
            )
            return True
        except Exception as e:
            print("Error in add_documents",e)
            return None

    def add_texts(self, text, collection_name) -> bool:
        try:
            self.client.from_texts(
                texts=[text],
                embedding=self.embedding,
                collection_name=collection_name,
                persist_directory="chroma",
            )
            return True
        except Exception as e:
            print("Exception in add_texts",e)
            return None


    def get_total_vector_count(self) -> int:
        try:
            return len(self.client.get()["documents"])
        except Exception as e:
            print("Exception in get_total_vector_count",e)
            return None

    def get_retriever(self, collection_name):
        try:
            return self.client.as_retriever(
                collection_name=collection_name, search_kwargs={"k": 3}
            )
        except Exception as e:
            print("Exception in get_retriever",e)
            return None

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]


    async def retrieve_data_with_chat_history(self, retriever, query, sid, user_id):
        try:
            await ChatHistory().insert_chat_history(
                user_id,
                query,
                'user'
            )
            
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, CONTEXTUALIZE_Q_PROMPT
            )
            question_answer_chain = create_stuff_documents_chain(self.llm, QA_PROMPT)
            rag_chain = create_retrieval_chain(
                history_aware_retriever, question_answer_chain
            )

            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
            )
            
            query_response = conversational_rag_chain.invoke(
                {"input": query},
                config={"configurable": {"session_id": str(sid)}},
            )["answer"]
            
            await ChatHistory().insert_chat_history(
                user_id,
                query_response,
                'assistant'
            )
            
            return query_response
        except Exception as e:
            print("Exception in retrieve_data_with_chat_history",e)
            return None

    def delete_collection(self) -> bool:
        try:
            self.client.delete_collection()
            return True
        except Exception as e:
            print("Exception in delete_collection",e)
            return None

