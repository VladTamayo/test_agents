
import os
from gradio.components import label
from httpx import delete
from openai import OpenAI
import gradio as gr
from gtts import gTTS
import tempfile

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4.5-preview-2025-02-27"

client = OpenAI()

client.api_key = os.environ['OPENAI_API_KEY']

with open("./files/only_llm.txt", "r") as file:
    instructions = file.read()

messages=[
    {"role": "developer", "content": instructions},
    ]

def get_completion(model:str, messages:list):
    completion = client.chat.completions.create(
        model = model,
        messages = messages
    )
    llm_completion = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": llm_completion})
    tts = gTTS(llm_completion, lang="en-AU")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return llm_completion, temp_audio.name

def get_chat_message(message, history):
    messages.append({"role": "user", "content": message})
    bot_message, audio = get_completion(llm_model, messages)
    return bot_message, audio

test_chat = gr.Interface(
    fn=get_chat_message,
    # type="messages",
    inputs="text",
    outputs=["text", gr.Audio( label="Audio response", autoplay=True)],
    # autofocus=True,
    # additional_outputs=[gr.Audio(label="Audio response", autoplay=True)]
)

if __name__ == "__main__":
    test_chat.launch(share=False)
