# Overview

This repository implements an evaluation pipeline to assess whether LLMs can analyze student Python code, generate conceptual prompts, surface misconceptions, and encourage reflective learning without giving away solutions. Three models are compared: 
* DeepSeek-V3 
* Llama 3.1 (405B)
* OpenAI GPT-OSS-20B.



# Setup

## 1) Clone the repository
    ```
    git clone https://github.com/ishit-10/fosse_researchWork_python.git
    cd fosse_researchWork_python
    ```

## 2) Create Python environment (using venv)
    ```
    python3.10 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    ```

## 3) Install Dependencies
    ```
    transformers>=4.30.0
    torch>=2.0.0
    pylint
    ```
    
  ### Install:
    ```
    pip install -r requirements.txt
    ```
  ### Other tools:
    ```
    pip install vllm accelerate huggingface_hub astpretty jupyter
    ```

## 4) Obtain model checkpoints
### Hugging Face login:
  ```
  huggingface-cli login
  ```
### Example (replace repo names with exact repos)
  ```
  # Deepseek-V3
  git lfs install
  huggingface-cli repo clone deepseek-ai/deepseek-v3
  ```
  ```
  # Llama 3.1 (Meta)
  huggingface-cli repo clone meta-llama/Llama-3-1
  ```
  ```
  # GPT-OSS-20B
  huggingface-cli repo clone openai/gpt-oss-20b
  ```




