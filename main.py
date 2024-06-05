from taipy.gui import Gui
import pandas as pd
import openai
import os
import time
import google.generativeai as palm
from audioInterp import *
from audioInterp import get_top_emotions
# openai.api_key="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"


# def get_completion(prompt, model="gpt-3.5-turbo"):
#     print(prompt)
#     messages = [
#         {"role": "system",
#          "content": "You are an interviewer preparing questions"
#         },
#         {"role": "user", 
#         "content": f"Give me 5 interview questions for this job position: {prompt}"}]
#     response = openai.ChatCompletion.create(
#     model=model,
#     messages=messages,
#     temperature=0
#     )
#     return response.choices[0].message["content"]


# prompt = ""
# prompt2 = ""
# content = ""

# # response = get_completion(prompt)


# uncomment to use the key palm.configure(api_key='AIzaSyCD1XlRiMH_Him5MdqNqtRvtuOhDe9TGr8')

# Get the first model that supports text generation
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model_name = models[0].name


def get_completion(prompt, model=model_name):
    complete_prompt = f"You are an HR and interview coach. Based on the job role '{prompt}', suggest 5 technical interview questions and 5 generally asked job specific."
    response = palm.generate_text(
        model=model,
        prompt=complete_prompt,
        temperature=0
    )
    return response.result

def get_emotion_feedback(emotions, prompt, model=model_name):
    emotion_list = ", ".join([emotion['name'] for emotion in emotions])
    complete_prompt = f"You are an HR and interview coach. Based on the detected emotions ({emotion_list}) and the job role '{prompt}', suggest how the candidate can improve their interview performance and provide feedback on technical aspects.Provide Specific areas of improvement and how they can achieve and also elaborate about important skills and their industry relevance based on their industry and job role"
    response = palm.generate_text(
        model=model,
        prompt=complete_prompt,
        temperature=0
    )
    return response.result

prompt = ""
prompt2 = ""
content = ""

# Example usage
response = get_completion(prompt)
print(response)


def test(state):
    state.prompt2 = state.prompt
    x = get_completion(state.prompt2)
    state.returnVal = '\n\n'.join(x.split('\n')) 
    
def printer(state):
    # state.value = state.content
    state.value = get_top_emotions(run(state.content))
    predictions = run(state.content)
    emotions = get_top_emotions(predictions)
    state.value = emotions
    state.emotion_feedback = get_emotion_feedback(emotions, state.prompt)
    # Format emotions into a string
    emotion_str = "\n".join([f"{emotion['name']}: {emotion['score']}" for emotion in emotions])
    state.value = emotion_str
    state.emotion_feedback = get_emotion_feedback(emotions, state.prompt)
    #state.value = get_top_emotions(run(state.content))

def change(state):
    state.value = "Submitted!"

value = "Insert File..."
returnVal = ""
emotion_feedback = ""
page = """

<center><|Generate interview questions|text|id=hdr|></center>
#
<center><|{prompt}|input|id=enter|label=Job Title|><|Generate Interview Questions|button|on_action=test|></center>
#
<center><|{returnVal}|input|id=response|label=Awaiting AI Response...|active=False|multiline=True|height=50|></center>

"""
page_file = """
<center><|AI Analyzations of your responses|text|id=hdr1|></center>

#
<center><|Upload a video of you answering the questions for, the previous page to receive feedback|></center>
#
<center><|The top 5 emotions the AI detected were:|text|></center>
<center><|{value}|text|id=hi|></center>
<center><|{content}|file_selector|extensions=.mp3,.mp4,.m4a|on_action=change|></center>
<center><|Submit|button|on_action=printer|></center>
<center><|Emotion Feedback:|text|></center>
<center><|{emotion_feedback}|text|id=emotion_feedback|multiline=True|height=100|></center>
"""

pages = {
    "/": "<|AscendAI|text|id=title|height=30px|width=30px|><|toggle|theme|>\n<center>\n<|navbar|>\n</center>",
    "generate-questions": page,
    "receive-feedback": page_file,
}


Gui(pages=pages).run(use_reloader=True, port=5001) 
