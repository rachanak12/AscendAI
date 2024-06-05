import pandas as pd
import openai
import os
import time
import google.generativeai as palm
openai.api_key="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"
palm.configure(api_key='AIzaSyCD1XlRiMH_Him5MdqNqtRvtuOhDe9TGr8')


models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model_name = models[0].name

def get_completion(prompt, model=model_name):
    print(prompt)
    # Prepare the messages as required by the PaLM API
    messages = [
        {"role": "system", "content": "You are an interviewer preparing questions"},
        {"role": "user", "content": f"Give me 5 interview questions for this job position: {prompt}"}
    ]

    # Call the PaLM API's generate text method
    response = palm.generate_text(
        model=model,
        messages=messages,
        temperature=0
    )

    # Extract the generated content from the response
    return response['result']


prompt = "What is 5 + 5?"

response = get_completion(prompt)
print(response)