from abc import ABC, abstractmethod
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List

class BaseVectorDB(ABC):

    @classmethod
    @abstractmethod
    def add_documents(self,file_path,collection) -> bool : ...

    @classmethod
    @abstractmethod
    def add_texts(self,texts : List[str], collection_name : str) -> bool : ...


    @classmethod
    @abstractmethod
    def get_total_vector_count(self) -> int : ...


    @classmethod
    @abstractmethod
    def retrieve_data_with_chat_history(self,retriever,query) -> str : ...


    @classmethod
    @abstractmethod
    def delete_collection(self,collection_name) -> bool : ...


    @classmethod
    @abstractmethod
    def get_retriever(self,collection) -> VectorStoreRetriever : ...
