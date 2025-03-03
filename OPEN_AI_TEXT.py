from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key with error checking
api_key = os.getenv('OPENAI_API_KEY').strip()
client = OpenAI(api_key=api_key)

# Generate a text completion
def get_completion(prompt, model="gpt-4o"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
            {"role": "system", "content": "You are Dr. Seuss.Write a bedtime story for a young child with whimsical rhymes. Always keep the story 100 words or less."},
            {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        raise

def filename_from_input(title):
  alphanum = ""
  for character in title:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)