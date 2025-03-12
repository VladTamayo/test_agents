import os
from openai import OpenAI
# import gradio

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
# openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = "gpt-3.5-turbo"

client = OpenAI()

client.api_key = os.environ['OPENAI_API_KEY']

messages=[
    {"role": "developer", "content": "You are a math tutor for children from 7 to 12 years, ask for child's in the first interaction, use a language based on he child's age. DO NOT other things that are not related to your role as a math tutor"},
    ]

def get_completion(model:str, messages:list): 
    completion = client.chat.completions.create(
        model = model,
        messages = messages
    )
    # print(messages)
    llm_completion = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": llm_completion})
    return llm_completion

# print("🤖: Hi, I'm you math tutor. How can I help you?")

while True:
    user_message = input("👨: ")
    if user_message == "/bye":
        break
    else:
        messages.append({"role": "user", "content": user_message})
        bot_message = get_completion(llm_model, messages)
        print("🤖: ", bot_message)



# def get_completion(prompt, model=llm_model):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0
#     )
#     return response.choices[0].message["content"]
#
# print(get_completion("What is 2+2?"))
