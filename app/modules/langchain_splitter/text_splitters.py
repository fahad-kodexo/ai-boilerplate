from langchain_text_splitters import (RecursiveCharacterTextSplitter,
                                      CharacterTextSplitter)

from typing import List


class Splitters:
    def __init__(self,splitter_type):
        self.splitter_type = splitter_type

    def splits(self,docs,chunk_size:int,chunk_overlap:int) -> List[str]:
        if self.splitter_type.lower() == "recursive_splitter":
            splitter =  RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
                )
        elif self.splitter_type.lower() == "character_splitter":
            splitter = CharacterTextSplitter(
                chunk_size = chunk_size,
                chunk_overlap=chunk_overlap
            )
        else:
            raise ValueError

        return splitter.split_documents(docs)
