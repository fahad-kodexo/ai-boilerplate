import traceback
from openai import OpenAI
from app.utils.constants import OPENAI_KEY
from app.utils.responses import emit_response
from typing_extensions import override
from openai import AssistantEventHandler

client = OpenAI(api_key=OPENAI_KEY)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, flush=True, end="")

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


class Assistant:
    @staticmethod
    async def create_assistant():
        try:
            return client.beta.assistants.create(
                name="QA Chatbot Assistant",
                instructions="You are an assistant for question-answering tasks in the documents. for irrelevant questions respond with sorry i don't know",
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                temperature=0.6,
            ).model_dump_json()
        except Exception as e:
            print("Error in create_assistant", e)
            return None

    @staticmethod
    async def upload_files(vector_store_name, file_paths, assistant_id):
        try:
            vector_store = client.beta.vector_stores.create(name=vector_store_name)

            file_streams = [open(path, "rb") for path in file_paths]

            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )

            _ = client.beta.assistants.update(
                assistant_id=assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )

            return file_batch.status
        except Exception as e:
            print("Error in upload_files", e)
            return None

    @staticmethod
    async def create_thread():
        try:
            return client.beta.threads.create().model_dump_json()
        except Exception as e:
            print("Error in create_thread", e)
            return None

    @staticmethod
    async def ask_query(query: str, thread_id: str, assistant_id: str, sio):
        try:
            _ = client.beta.threads.messages.create(
                thread_id=thread_id, role="user", content=query
            )

            with client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions="You are an assistant for question-answering tasks in the documents. for irrelevant questions respond with sorry i don't know",
                event_handler=EventHandler(),
            ) as stream:
                for stream_text in stream.text_deltas:
                    if stream_text is None:
                        await emit_response(sio, "query_response", "")
                    else:
                        await emit_response(sio, "query_response", stream_text)

                return True

        except Exception as e:
            print("Error in ask_query", traceback.print_exc())
            await emit_response(sio, "query_response", "")
            return None
