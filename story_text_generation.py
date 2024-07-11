from openai import OpenAI
import os


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

def filename_from_input(title):
  alphanum = ""
  for character in title:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)