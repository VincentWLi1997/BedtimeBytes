from openai import OpenAI

client = OpenAI(api_key='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')

# Generate a text completion
def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "Write a bedtime story for a young child"},
        {"role": "user", "content": prompt},
        ]
    )
   return completion.choices[0].message.content

def generate(prompt):
   response = get_completion(prompt)
   return response