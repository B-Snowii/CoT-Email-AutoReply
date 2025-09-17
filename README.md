# CoT Email AutoReply Engine

[![Language](https://img.shields.io/badge/Language-English-blue)](README.md)
[![语言](https://img.shields.io/badge/语言-中文-red)](README.zh-CN.md)


## 🚀 Overview

This project demonstrates the evolution from basic prompting to Chain of Thought (CoT) reasoning, achieving a remarkable improvement from 16.7% to 100% accuracy, representing an 83.3% performance enhancement.

## 🏗️ System Architecture

```
Received Email → CoT Reasoning Engine → Decision Matrix → Response Generator
     ↓                    ↓                    ↓              ↓
Message Analysis → Step-by-step Logic → Reply/Response/Action → Email Output
```

**Core Functionality:**
- **Reply Decision**: Determine whether to reply to emails (Yes/No)
- **Response Generation**: Generate appropriate email responses when needed
- **Action Classification**: Decide on appropriate actions based on email content

**Application Scenarios:** Academic paper inclusion requests, Business email automation, Customer service responses, General email management

## 🔬 Research Evolution

| Version | Model | Approach | Reply Accuracy | Response Accuracy | Action Accuracy | Overall Score | File |
|---------|-------|----------|----------------|------------------|-----------------|---------------|------|
| **V1** | Flan-T5-Large | Basic Prompting | **25%** | **0%** | **25%** | **16.7%** | `V1-Flan-T5-Large.py` |
| **V2** | DeepSeek R1 | Basic Prompting | **50%** | **25%** | **50%** | **41.7%** | `V2-DS.py` |
| **V3** | Llama2 | CoT Reasoning | **75%** | **50%** | **100%** | **75.0%** | `V3-Llama2-CoT.py` |
| **V4** | DeepSeek R1 | CoT Reasoning | **100%** | **100%** | **100%** | **100%** | `V4-DS-CoT.py` |

## 🧠 CoT Reasoning Framework

The system uses a structured 4-step reasoning process:

```
Step 1: Strong Rejection Check
- Did the email sender give us strong rejection? (Yes/No)

Step 2: Attitude Clarity Assessment  
- Is the email sender's attitude clear? (Positive/Negative)

Step 3: Information Requirements
- Is further information required? (Yes/No)

Step 4: Decision Synthesis
- Based on analysis, determine Reply/Response/Action
```





## 📄 License

This project is licensed under the MIT License.

---
