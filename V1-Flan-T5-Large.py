import os
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig
import re

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

model_name='google/flan-t5-large'
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)#use the trained transformer model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

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
    "Below are several examples of ideal actions from previous data. "
    "Please carefully study these samples and generate a new reply, response, and action for the given message. "
    "All replies, responses, and actions should be generated strictly based on the message provided. "
    "Emulate the style, tone, and quality of the former examples. "
    "Your output MUST be in the following format, each on a new line: \n"
    "Reply: <your reply>\nResponse: <your response>\nAction: <your action>\n"
    "Format your output exactly as shown above.\n\n"
)

def generate_reply(message):
    prompt = (
        f"Message: {message}\n"
        "Should you reply to this message? Answer only 'Yes' or 'No'."
    )
    inputs = tokenizer(prompt, return_tensors='pt')
    output_ids = model.generate(
        inputs["input_ids"],
        top_k=2,
        do_sample=True
    )
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output.strip().split()[0]  # Only take the first word (Yes/No)

def generate_response(message, reply):
    if reply.lower() == 'no':
        return 'NA'
    prompt = (
        f"Message: {message}\n"
        f"Reply: {reply}\n"
        "Since you will reply, generate an appropriate response to this message."
    )
    inputs = tokenizer(prompt, return_tensors='pt')
    output_ids = model.generate(
        inputs["input_ids"],
        temperature=0.1,
        top_k=3,
        do_sample=True
    )
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output.strip()

def generate_action(message, reply, response):
    prompt = (
        f"Message: {message}\n"
        f"Reply: {reply}\n"
        f"Response: {response}\n"
        "Based on the message, reply, and response above, should this paper be included? Answer only 'Include' or 'Do not include'."
    )
    inputs = tokenizer(prompt, return_tensors='pt')
    output_ids = model.generate(
        inputs["input_ids"],
        top_p=0.4,
        do_sample=True
    )
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip().lower()
    if 'do not' in output:
        return 'Do not include'
    elif 'include' in output:
        return 'Include'
    else:
        return output.capitalize()

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
