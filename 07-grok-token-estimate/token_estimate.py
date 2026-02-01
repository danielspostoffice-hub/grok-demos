import pandas as pd
from pathlib import Path

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

# Rough token estimate (1 token ~4 chars English + overhead)
df['tokens'] = (df['content_trunc'].str.len() // 3) + 10  # Conservative +10 per message

total_tokens = df['tokens'].sum()
user_tokens = df[df['role'].str.contains('human|user', case=False, na=False)]['tokens'].sum()
assistant_tokens = df[df['role'].str.contains('assistant|grok', case=False, na=False)]['tokens'].sum()

print(f"Estimated total tokens: {total_tokens:,}")
print(f"User input tokens: {user_tokens:,}")
print(f"Grok output tokens: {assistant_tokens:,}")

# Rough cost (grok-4 approx $10/M input, $30/M output—check docs for current)
input_cost = user_tokens / 1_000_000 * 10
output_cost = assistant_tokens / 1_000_000 * 30
total_cost = input_cost + output_cost
print(f"\nRough cost estimate: ${total_cost:.2f} (input ${input_cost:.2f} + output ${output_cost:.2f})")