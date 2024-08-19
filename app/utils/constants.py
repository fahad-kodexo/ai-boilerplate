import os

from dotenv import load_dotenv
from app.utils.config_utils import read_config

load_dotenv()
config_data = read_config()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
STRIPE_KEY = os.getenv("STRIPE_KEY")
ENDPOINT_SECRET = os.getenv("ENDPOINT_SECRET")
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
SUCCESS_URL = os.getenv("SUCCESS_URL")

EMBEDDING_MODEL = config_data["EMBEDDING_MODEL"]
LLM_MODEL  = config_data["LLM_MODEL"]
SUBJECT = config_data["SUBJECT"]
CHARSET = config_data["CHARSET"]
CHUNK_SIZE = config_data["CHUNK_SIZE"]
CHUNK_OVERLAP = config_data["CHUNK_OVERLAP"]
SPLITTER = config_data["SPLITTER"]
TEMPERATURE = config_data["TEMPERATURE"]
LOADER = config_data["LOADER"]


ROLE = "user"
ASSISTANT_NAME = "Question answering Chatbot"
HISTORY_COLLECTION_NAME = "chat_historyy"

PROMPT_DICT = {
            "bot": """
            Answer the question based on the following context and conversation_history : 

            context : {prompt}

            <instructions>
            1. If the user asks an off-topic question , respond with: "I don't have information about [user's query]"
            </instructions>

            <conversation_history>
            {history}
            <conversation_history>
            {input}

            """}