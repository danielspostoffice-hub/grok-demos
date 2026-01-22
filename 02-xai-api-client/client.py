import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise ValueError("XAI_API_KEY not set in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1"
)

prompt = "Explain why xAI's mission matters in one paragraph."

response = client.chat.completions.create(
    model="grok-4",  # Verify current model name at https://docs.x.ai/docs/models if error
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500,
    temperature=0.7
)

print("Prompt:", prompt)
print("\nGrok response:")
print(response.choices[0].message.content)
