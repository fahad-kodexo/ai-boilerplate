import traceback
from app.utils.constants import (
    OPENAI_KEY,
    EMBEDDING_MODEL,
    LLM_MODEL,
    LOADER,
    SPLITTER,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TEMPERATURE,
    PROMPT_DICT,
)
from app.vector_db_operations.base import BaseVectorDB
from app.chat_history.db import ChatHistory

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.utils.langchain_utils import Loaders
from app.utils.langchain_utils import Splitters
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

from app.chat_history.db import ChatHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate

import warnings
import time

warnings.filterwarnings("ignore")


class ChromaDb(BaseVectorDB):
    # embedding = OpenAIEmbeddings(api_key=OPENAI_KEY)
    embedding = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMPERATURE, api_key=OPENAI_KEY)

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
            print("Error in add_documents", e)
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
            print("Exception in add_texts", e)
            return None

    def get_total_vector_count(self) -> int:
        try:
            return len(self.client.get()["documents"])
        except Exception as e:
            print("Exception in get_total_vector_count", e)
            return None

    def get_retriever(self, collection_name):
        try:
            return self.client.as_retriever(
                collection_name=collection_name, search_kwargs={"k": 2}
            )
        except Exception as e:
            print("Exception in get_retriever", e)
            return None

    async def retrieve_data_with_chat_history(self, query, sio, user_id):
        try:
            doc_result = self.client.similarity_search(query, k=3)
            document_context = ""
            for document in doc_result:
                text = document.page_content.replace("\n", "")
                document_context += text

            chat_data = await ChatHistory().get_chat_history(user_id)
            chat_history = ChatMessageHistory()

            for chat in chat_data["chat_history"]:
                if chat["type"] == "user":
                    chat_history.add_user_message(chat["message"])
                else:
                    chat_history.add_ai_message(chat["message"])

            prompt_template = PROMPT_DICT["bot"].replace("{prompt}", document_context)

            PROMPT = PromptTemplate(
                input_variables=["history", "input"], template=prompt_template
            )
            memory = ConversationBufferMemory(
                chat_memory=chat_history, memory_key="history", return_messages=True
            )
            conversation = ConversationChain(
                llm=self.llm, verbose=False, memory=memory, prompt=PROMPT
            )

            query_response = conversation.stream(input=f"{query}")["response"]

            return query_response
        except Exception as e:
            print("Exception in retrieve_data_with_chat_history", traceback.print_exc())

            return None

    def delete_collection(self) -> bool:
        try:
            self.client.delete_collection()
            return True
        except Exception as e:
            print("Exception in delete_collection", e)
            return None
