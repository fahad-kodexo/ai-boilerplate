from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from app.utils.constants import system_prompt,contextualize_q_system_prompt


def create_prompt(prompt):
    QA_PROMPT = ChatPromptTemplate.from_messages(
                [
                    ("system", prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
    return QA_PROMPT

CONTEXTUALIZE_Q_PROMPT = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

