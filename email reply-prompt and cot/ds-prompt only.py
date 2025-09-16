import os
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig
import re
import requests

# Path to your Excel file (input data)
excel_path = os.path.join(os.path.dirname(__file__), "former.xlsx")

# Read the Excel file
# Columns: 0=Message, 1=Reply, 2=Response, 3=Action
# No header

df = pd.read_excel(excel_path, header=None)

# Extract rows (example: first row for each column)
message = df.iloc[0, 0]      # First row, Message
reply = df.iloc[0, 1]        # First row, Reply
response = df.iloc[0, 2]     # First row, Response
action = df.iloc[0, 3]       # First row, Action

dataset = {
    "message": message,
    "reply": reply,
    "response": response,
    "action": action
}

# Path to your sample file (same directory as this script)
sample_path = os.path.join(os.path.dirname(__file__), "train.xlsx")

# Read the Excel file, no header, so all rows are data
df_sample = pd.read_excel(sample_path, header=None)

# Extract columns: Message (0), Reply (1), Response (2), Action (3), skipping the first row
messages_ideal = df_sample.iloc[1:, 0]    # Column 0
replies_ideal = df_sample.iloc[1:, 1]     # Column 1
responses_ideal = df_sample.iloc[1:, 2]   # Column 2
actions_ideal = df_sample.iloc[1:, 3]     # Column 3

# Add DeepSeek API call function

def deepseek_generate(prompt, api_url, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "top_p": 0.9,        # Optional, for nucleus sampling
        "temperature": 0.3 
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Set your DeepSeek API endpoint and key
api_url = "https://api.deepseek.com/v1/chat/completions"
api_key = "sk-55eeddbe855140adbb74d8da8121bcb0"  # Replace with your API key or set to None

# Prepare few-shot examples from your training data
few_shot_examples = ""
for i in range(2):  # Use as many as you want for shots
    ex_message = str(df.iloc[i, 0])
    ex_reply = str(df.iloc[i, 1])
    ex_response = str(df.iloc[i, 2])
    ex_action = str(df.iloc[i, 3])
    few_shot_examples += (
        f"Message: {ex_message}\n"
        f"Reply: {ex_reply}\n"
        f"Response: {ex_response}\n"
        f"Action: {ex_action}\n\n"
    )

# Update instruction to explicitly require the output format
instruction = (
    "Objective: As a research assistant, classify emails from researchers about paper inclusion in the HKU Jockey Club Enterprise Sustainability Global Research Institute SSRN series. Determine:\n"
    "- Reply: Should a response be sent? ('Yes' or 'No')\n"
    "- Response: If replying, draft a formal email response. If not, return 'NA'.\n"
    "- Action: Final decision to 'include' or 'not include' the paper.\n\n"
    "Instructions:\n"
    "1. Determine 'Reply':\n"
    "   - Reply = 'Yes' ONLY if:\n"
    "     * Explicit removal/opt-out request ('Remove my papers')\n"
    "     * Technical/process questions ('Can you include published papers?')\n"
    "     * Cover page/affiliation issues\n"
    "   - Reply = 'No' if:\n"
    "     * Simple confirmation ('Proceed', 'Sounds great')\n"
    "     * No objection (no response by deadline)\n"
    "     * Brief acknowledgments ('Thanks')\n"
    "     * Passive opt-out ('Please don't include')\n\n"
    "2. Generate 'Response':\n"
    "   - If Reply = 'Yes':\n"
    "     * Removal requests: 'I've contacted SSRN to process your request...'\n"
    "     * Technical issues: 'We'll correct this immediately...'\n"
    "     * Questions: Answer concisely + offer help\n"
    "   - If Reply = 'No': Always return 'NA'\n\n"
    "3. Determine 'Action':\n"
    "   - 'include' if:\n"
    "     * Author confirms/doesn't object\n"
    "     * Paper aligns with sustainability\n"
    "   - 'not include' if:\n"
    "     * Explicit opt-out/removal request\n"
    "     * Paper irrelevant to sustainability\n\n"
    "Format EXACTLY as:\n"
    "Reply: <Yes/No>\nResponse: <response text or NA>\nAction: <include/not include>"
)

def generate_reply(message):
    prompt = (
        f"Message: {message}\n"
        "Should you reply to this message? Answer only 'Yes' or 'No'."
    )
    output = deepseek_generate(prompt, api_url, api_key)
    return output.strip().split()[0]  # Only take the first word (Yes/No)

def generate_response(message, reply):
    if reply.lower() == 'no':
        return 'NA'
    prompt = (
        f"Message: {message}\n"
        f"Reply: {reply}\n"
        "Since you will reply, generate an appropriate response to this message."
    )
    output = deepseek_generate(prompt, api_url, api_key)
    return output.strip()

def generate_action(message, reply, response):
    prompt = (
        f"Message: {message}\n"
        f"Reply: {reply}\n"
        f"Response: {response}\n"
        "Based on the message content and workflow rules, should this paper be included in the SSRN series?\n"
        "Return ONLY 'include' or 'not include' based on these criteria:\n"
        "- 'include' if: confirms inclusion, no objection, paper aligns with sustainability\n"
        "- 'not include' if: opt-out request, paper irrelevant to sustainability\n"
    )
    output = deepseek_generate(prompt, api_url, api_key).strip().lower()
    # Normalization logic
    if 'not include' in output or 'opt-out' in output or 'remove' in output:
        return 'not include'
    elif 'include' in output or 'proceed' in output or 'confirm' in output:
        return 'include'
    else:  # Fallback for ambiguous responses
        return 'include' if reply.lower() == 'no' else 'not include'

# Generate reply, response, and action for each row in train.xlsx and write to columns 1, 2, 3
for idx in range(1, len(df_sample)):
    message = str(df_sample.iloc[idx, 0])      # Column 0
    reply_gen = generate_reply(message)
    response_gen = generate_response(message, reply_gen)
    action_gen = generate_action(message, reply_gen, response_gen)
    df_sample.iloc[idx, 1] = reply_gen
    df_sample.iloc[idx, 2] = response_gen
    df_sample.iloc[idx, 3] = action_gen
    print(f"Processed row {idx}: Reply: {reply_gen} | Response: {response_gen} | Action: {action_gen}")

# Ensure df_sample has at least 5 columns (index 0-4)
if df_sample.shape[1] < 5:
    for _ in range(5 - df_sample.shape[1]):
        df_sample[df_sample.shape[1]] = ""


# Save the updated DataFrame back to Excel
df_sample.to_excel(os.path.join(os.path.dirname(__file__), "train_with_outcomes.xlsx"), header=None, index=False)
