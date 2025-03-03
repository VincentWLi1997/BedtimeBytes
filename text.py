from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Get API key and improve debugging
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Make sure OPENAI_API_KEY is set in your .env file")

# Clean the API key by removing any whitespace or newlines
api_key = api_key.strip()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def main():
    try:
        # Get user input
        user_topic = input("What would you like me to write about? ")
        
        print("\nGenerating response...")
        print("Using API key (first 5 chars):", api_key[:5] + "...")
        
        # Make API call
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep your response to exactly 30 words."},
                {"role": "user", "content": f"Write 30 words about: {user_topic}"}
            ],
            timeout=30  # Add timeout to catch connection issues
        )
        
        # Print the response
        print("\nHere's your 30-word response:")
        print(completion.choices[0].message.content)
        
    except ValueError as ve:
        print(f"\nConfiguration error: {str(ve)}")
    except TimeoutError:
        print("\nConnection timed out. Please check your internet connection.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    main()