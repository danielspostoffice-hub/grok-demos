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

initial_prompt = (
    "Estimate the number of piano tuners in New York City. "
    "Show your step-by-step reasoning and arrive at a final number."
)

messages = [{"role": "user", "content": initial_prompt}]

print("Initial prompt:")
print(initial_prompt)
print("\n" + "="*80 + "\n")

for i in range(5):  # Initial + 4 critique loops = 5 total turns
    response = client.chat.completions.create(
        model="grok-4",  # Worked in 02
        messages=messages,
        max_tokens=800,
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    print(f"Turn {i+1} - Grok:")
    print(reply)
    print("\n" + "-"*80 + "\n")
    
    if i == 4:
        break
    
    critique = (
        "Previous answer:\n\n"
        f"{reply}\n\n"
        "Critique it: find errors, weak assumptions, missing factors. "
        "Then give improved reasoning and refined final estimate."
    )
    messages.append({"role": "assistant", "content": reply})
    messages.append({"role": "user", "content": critique})

print("Chain complete. Final refined estimate in Turn 5.")