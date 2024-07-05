import os

from dotenv import load_dotenv
from app.utils.utils import read_config

load_dotenv()
config_data = read_config()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
STRIPE_KEY = os.getenv("STRIPE_KEY")
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
AWS_REGION = os.getenv("AWS_REGION")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_ACCESS_KEY  = os.getenv("SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
LLAMA_PARSER_API = os.getenv("LLAMA_PARSER_API")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
JINA_READER_API_KEY = os.getenv("JINA_READER_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

EMBEDDING_MODEL = config_data["EMBEDDING_MODEL"]
LLM_MODEL  = config_data["LLM_MODEL"]
EMAIL_SERVICE = config_data["EMAIL_SERVICE"]
SUBJECT = config_data["SUBJECT"]
CHARSET = config_data["CHARSET"]
CHUNK_SIZE = config_data["CHUNK_SIZE"]
CHUNK_OVERLAP = config_data["CHUNK_OVERLAP"]
SPLITTER = config_data["SPLITTER"]
TEMPERATURE = config_data["TEMPERATURE"]
LOADER = config_data["LOADER"]


contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

