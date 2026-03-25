# 🛡️ LLM Prompt Injection Guard (RAG-Based)

> A **Retrieval-Augmented Prompt Injection Guard** that detects and prevents malicious prompts targeting Large Language Models by grounding decisions in explicit security policies.
> This system combines semantic retrieval, policy-aware reasoning, and enforcement control to create an interpretable and extensible guardrail architecture for LLM applications.
![Dashboard](assets/PARL.png)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-local%20inference-black?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 Motivation

Modern LLM systems are vulnerable to prompt injection attacks such as:

* instruction override
* role escalation
* system prompt extraction
* memory leakage
* tool invocation abuse
* data exfiltration

Most defenses rely on static heuristics or model behavior constraints.

This project explores a **policy-grounded RAG architecture** where security decisions are:

* explainable
* auditable
* extensible
* decoupled from model internals

---

## 🧠 System Architecture

```
Policy Corpus
   ↓
Semantic Chunking
   ↓
Embedding Memory
   ↓
Policy Retrieval
   ↓
Policy Evaluator (LLM reasoning)
   ↓
Enforcement Engine
   ↓
Secure Runtime Generation
   ↓
Observability Dashboard
```

### Key Idea

Security policies are treated as **retrievable knowledge**, allowing the system to dynamically reason about violations rather than rely on static filtering.

---

## ✨ Features

### 🔍 Policy-Grounded Detection

Retrieves relevant security policies before evaluating prompts.

### 🧠 LLM-Based Policy Reasoning

Uses an LLM to classify violations using retrieved policy context.

### 🚫 Enforcement Layer

Maps policy violations to runtime actions:

| Decision | Behavior             |
| -------- | -------------------- |
| allow    | normal generation    |
| warn     | generation + notice  |
| restrict | sanitized generation |
| block    | refusal              |

### ⚡ Streaming Secure Responses

Token streaming enabled for permitted generations.

### 📊 Evaluation Framework

Includes dataset-based evaluation measuring:

* detection accuracy
* precision / recall
* false positive rate
* policy attribution accuracy

### 🖥️ Guard Dashboard

Interactive Streamlit interface exposing:

* prompt
* retrieved policies
* reasoning
* risk classification
* final response

---

## 📁 Project Structure

```
LLM-Prompt-Injection-Guard/
│
├── policies/                # Security policy corpus
├── rag_guard/
│   ├── ingestion/           # Policy chunking & embedding
│   ├── retrieval/           # Semantic policy retrieval
│   ├── evaluation/          # Policy reasoning evaluator
│   ├── enforcement/         # Decision enforcement engine
│   ├── runtime/             # Secure generation wrapper
│   ├── pipeline/            # End-to-end guard pipeline
│   └── observability/       # Guard event logging
│
├── evaluation/              # Dataset & evaluation scripts
├── app.py             # Streamlit guard dashboard
└── README.md
```

---

## ⚙️ Setup

### 1. Create environment

```
python -m venv .venv
```

Activate:

```
.venv\Scripts\activate
```

### 2. Install dependencies

```
pip install streamlit langchain langchain-core langchain-community langchain-ollama chromadb pandas
```

### 3. Start Ollama

Ensure local Ollama server is running:

```
ollama serve
```

Pull models:

```
ollama pull gemma3
ollama pull mxbai-embed-large
```

---

## ▶️ Usage

### Build policy memory

```
python -m rag_guard.ingestion.build_index
```

### Run dashboard

```
streamlit run app.py
```

### Evaluate guard

```
python -m rag_guard.evaluation.run_eval
```

---

## 📊 Evaluation

Evaluation uses a curated adversarial dataset covering:

* system prompt extraction
* jailbreak attempts
* role escalation
* memory leakage
* sensitive data exposure

Metrics computed:

* accuracy
* precision
* recall
* F1 score
* false positive rate
* policy attribution accuracy

---

## 🔬 Research Insights

This project demonstrates:

* RAG can be applied to **security policy grounding**
* policy retrieval improves interpretability of guard decisions
* separation of detection and enforcement improves modularity
* guard-controlled generation is critical for real defense

---

## 🚧 Future Work

* adversarial prompt generation
* multi-step attack simulation
* tool-level runtime guard
* dynamic policy updates
* policy conflict resolution
* guard confidence calibration

---

## 📜 License

MIT License
