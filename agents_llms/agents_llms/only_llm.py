import os
from openai import OpenAI
# import gradio

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

def get_completion(model:str, messages:list) -> str | None:
    completion = client.chat.completions.create(
        model = model,
        messages = messages
    )
    llm_completion = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": llm_completion})
    return llm_completion

print("Say Hi. If you want to stop type /bye")

while True:
    user_message = input("👨: ")
    if user_message == "/bye":
        break
    else:
        messages.append({"role": "user", "content": user_message})
        bot_message = get_completion(llm_model, messages)
        print("🤖: ", bot_message)
