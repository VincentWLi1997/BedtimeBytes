from openai import OpenAI
import os
import API_KEY


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Generate a text completion
def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "Write a bedtime story for a young child. Always keep the story 300 words or less."},
        {"role": "user", "content": prompt},
        ]
    )
   return completion.choices[0].message.content