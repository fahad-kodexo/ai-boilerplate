from langchain_community.document_loaders import (TextLoader,
                                                  PyPDFDirectoryLoader,
                                                  LLMSherpaFileLoader,
                                                  )



from app.utils.constants import LLAMA_PARSER_API,JINA_READER_API_KEY
from langchain.schema.document import Document
from langchain_text_splitters import (RecursiveCharacterTextSplitter,
                                      CharacterTextSplitter)
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
import requests
from typing import List
# set up parser
parser_client = LlamaParse(
    result_type="markdown",
    api_key=LLAMA_PARSER_API
    )


class Loaders:
    encoding = "utf-8"
    file_extractor = {".pdf": parser_client}
    def __init__(self, loader_type:str = "llama_parser", webloader_type:str = "reader") -> None:
        self.loader_type = loader_type
        self.webloader_type = webloader_type


    def fetch_content_with_reader(self, input_url, headers=None):

        full_url = "https://r.jina.ai/" + input_url
        if headers is None:
            headers = {"Accept": "application/json",
                       "Authorization" : f"Bearer {JINA_READER_API_KEY}"}

        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()["data"]["content"],input_url  # Return the JSON response content
            else:
                return f"Request failed with status code {response.status_code}",None

        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}",None


    def load(self,file_path:str = None,url_path:str = None) -> Document:
        if self.loader_type == "text" and file_path is not None:
            return TextLoader(file_path=file_path,encoding=Loaders.encoding).load()
        elif self.loader_type == "pypdf" and file_path is not None:
            return PyPDFDirectoryLoader(file_path).load()
        elif self.loader_type == "llmsherpa" and file_path is not None:
            return LLMSherpaFileLoader(file_path).load()
        elif self.loader_type == "llama_parser" and file_path is not None:
            documents = SimpleDirectoryReader(input_files=[file_path],
                                               file_extractor=Loaders.file_extractor).load_data()
            text = documents[0].text
            metadata = documents[0].metadata
            # Wrapping the data into the Langchain Document Class
            docs = [Document(page_content=text,
                             metadata=metadata)]
            return docs
        elif self.webloader_type == "reader" and url_path is not None:
            url_content,url = self.fetch_content_with_reader(url_path)
            if url is None:
                raise ValueError
            print("url_content",type(url_content))
            print("Actual Data",url_content)
            docs = [Document(page_content=url_content)]
            print("docs",docs)
            return docs
        else:
            return None


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
