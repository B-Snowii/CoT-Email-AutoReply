import pandas as pd
import os
import re
import requests

# --- CoT Examples for Few-Shot Prompting ---
cot_examples = [
    {
        "example": "Dear Researcher, Thank you for this opportunity. I'll be happy to share my paper in your working paper series.",
        "step": "step1: did the professor give us strong rejection? No, so we could include it; step2: is the attitude of this professor clear? refer to 'I'll be happy to' and 'thank you for this opportunity', this is a clear positive attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "include"
    },
    {
        "example": "Hi Researcher, Sounds great, thank you!",
        "step": "step1: did the professor give us strong rejection? No, so we could include it; step2: is the attitude of this professor clear? refer to 'sounds great', this is a clear positive attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "include"
    },
    {
        "example": "Please dont. Paper is submitted to journal.",
        "step": "step1: did the professor give us strong rejection? Yes, so we should not include it; step2: is the attitude of this professor clear? refer to 'please don't', this is a clear negative attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    },
    {
        "example": "Thanks, Researcher. I'm happy to proceed with the inclusion of our paper in the Research Institute Paper Series.",
        "step": "step1: did the professor give us strong rejection? No, so we should include it; step2: is the attitude of this professor clear? refer to 'I'm happy' and 'thanks', this is a clear positive attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "include"
    },
    {
        "example": "Hi Researcher, The paper is not quite ready so please don't include it in the working paper series yet.  Thank you.",
        "step": "step1: did the professor give us strong rejection? Yes, so we should not include it; step2: is the attitude of this professor clear? refer to 'please don't', this is a clear negative attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    },
    {
        "example": "Of course! Please, go ahead!",
        "step": "step1: did the professor give us strong rejection? No, so we should include it; step2: is the attitude of this professor clear? refer to 'of course' and 'go ahead', this is a clear positive attitude; step3: is there any further information required to answer in this case?No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "include"
    },
    {
        "example": "Thanks, Researcher!  The paper also will be linked to the Academic Partner research paper series – please let me know if that is a problem.",
        "step": "step1: did the professor give us strong rejection? No, so we should include it; step2: is the attitude of this professor clear? refer to 'of course' and 'go ahead', this is a clear positive attitude; step3: is there any further information required  to answer in this case? Although it mentioned this paper is linked to Academic Partner research paper, but it will not influence the decision of our series inclusion, so further details required are no;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "include"
    },
    {
        "example": "...not the  'Example Research Paper Title'...this is Computer Science, not Sustainability.",
        "step": "step1: did the professor give us strong rejection? yes, so we should not include it; step2: is the attitude of this professor clear? refer to 'not the (title name)' , this is a clear negative attitude; step3: is there any further information required  to answer in this case? No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    },
    {
        "example": "Hi Researcher, This paper does not have content related to governance, social and sustainability themes so I do not think it should be included in the series. It is a pure empirical asset pricing paper.",
        "step": "step1: did the professor give us strong rejection? yes, so we should not include it; step2: is the attitude of this professor clear? refer to 'I do not think it should be included ' , this is a clear negative attitude; step3: is there any further information required  to answer in this case? No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    },
    {
        "example": "I chose to opt out of this inclusion. Thanks a lot.",
        "step": "step1: did the professor give us strong rejection? yes, so we should not include it; step2: is the attitude of this professor clear? refer to 'I chose to opt out ' , this is a clear negative attitude; step3: is there any further information required  to answer in this case? No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    },
    {
        "example": "I hope you are well? Could I ask you to see if you can update this paper on SSRN which is in both the Academic Partner and the Academic Institution series? You can find the Academic Partner pages on the attached version.",
        "step": "step1: did the professor give us strong rejection? No, he wants to include this paper both on Academic Partner and Academic Institution, and we're parts of Academic Institution; step2: is the attitude of this professor clear? refer to 'in both the Academic Partner and the Academic Institution series' , this is a clear positive attitude; step3: is there any further information required  to answer in this case? Yes, because it mentioned the cover/cover page from Academic Partner, and we will not add out cover page if there're cover pages from other institutes occurred, such as Academic Partner, Academic Partner(no matter which institute it is, we skip our cover page). We have to reply profs to make them sure we'll not add our cover page;step4: based on the clear attitude  but further required information/concerns, then we should reply to the professor, so, and the response is the email content we draft to professor in the meanwhile, we have to confirm we'll not add our cover page in these cases and be kindly",
        "Reply": "Yes",
        "Response": "We typically skip the cover page for Academic Partner-covered papers because we understand how much the Academic Partner recognition means to researchers. (optional, if Academic Partner mentioned) Professor made a specific remark and reminder on this.",
        "action": "include"
    },
    {
        "example": "Hi Researcher thanks for picking this up. I'd rather wait until we post the next version in the autumn which will contain findings from interviews. This is currently very much a framework paper. Best wishes. Dr. Smith",
        "step": "step1: did the professor give us strong rejection? Yes, refer to 'I'd rather wait', so we should not include; step2: is the attitude of this professor clear? refer to 'I'd rather wait', this is a clear negative attitude; step3: is there any further information required  to answer in this case? No;step4: based on the clear attitude and no further required information/concerns, then we should not reply to the professor, so the reply is no, and the response is the email content we draft to professor, therefore will be NA, it means not available.",
        "Reply": "No",
        "Response": "NA",
        "action": "not include"
    }
]

# --- Few-shot prompt construction ---
def build_few_shot_prompt(message):
    prompt = "Background: You are a research assistant at the HkU Jokey Club Enterprise Sustainability Global Research Institute. Below are several examples with step-by-step reasoning for classifying inclusion emails. \n\n"
    for ex in cot_examples:
        prompt += f"Example: {ex['example']}\nStep: {ex['step']}\nReply: {ex['Reply']}\nResponse: {ex['Response']}\nAction: {ex['action']}\n\n"
    prompt += f"Make sure you've totally understood the examples above, and then answer the following question by considering step by step: Example: {message}\nProvide the related reply, response, and action seperately."
    return prompt


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
        "top_p": 0.9, 
        "top_k": 25,       
        "temperature": 0.3 
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Set your DeepSeek API endpoint and key
api_url = "https://api.deepseek.com/v1/chat/completions"
api_key = "sk-55eeddbe855140adbb74d8da8121bcb0"  # Replace with your API key or set to None

# Only keep the function to generate answers for a single message

def generate_answers(message):
    prompt = build_few_shot_prompt(message)
    output = deepseek_generate(prompt, api_url, api_key).strip()
    return output


if __name__ == "__main__":
    sample_path = os.path.join(os.path.dirname(__file__), "train.xlsx")
    df_sample = pd.read_excel(sample_path, header=None)
    messages_ideal = df_sample.iloc[1:, 0]  # Skip header if present
    for idx, message in enumerate(messages_ideal, start=1):
        print(f"\n--- Message {idx} ---")
        print(f"Input: {message}")
        result = generate_answers(str(message))
        print("Output:")
        print(result)
        print("-------------------")

