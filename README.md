# Setup Instructions & Reasoning

This repository implements an evaluation pipeline to assess whether LLMs can analyze student Python code, generate conceptual prompts, surface misconceptions, and encourage reflective learning without giving away solutions. Three models are compared: DeepSeek-V3, Llama 3.1 (405B), and OpenAI GPT-OSS-20B.

# Setup
1) Clone the repository
   `git clone https://github.com/ishit-10/fosse_researchWork_python.git
cd fosse_researchWork_python
`

2) Create Python environment (using venv)
   `python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
`

3) Install Dependencies
   `transformers>=4.30.0
torch>=2.0.0
pylint
`
`pip install -r requirements.txt
`
 Other tools:
 `pip install vllm accelerate huggingface_hub astpretty jupyter
`

4) Obtain model checkpoints:
   (A) Login on Hugging Face
       `huggingface-cli login
`
   Example (replace repo names with exact repos):
       # DeepSeek-V3
         `git lfs install
huggingface-cli repo clone deepseek-ai/deepseek-v3`
       # Llama 3.1 (Meta)
         `huggingface-cli repo clone meta-llama/Llama-3-1`
       # GPT-OSS-20B
         `huggingface-cli repo clone openai/gpt-oss-20b`
   
6) Run the evaluation script
   A simple CLI wrapper 'run_eval.py' should accept a model identifier and a code file, then store outputs to 'results/<model_name>/<timestamp>.json'
   (Replace placeholders with path to local files)
   Example usage for deepseek-v3:
      `python run_eval.py \
  --model deepseek-v3 \
  --checkpoint /path/to/deepseek-v3/checkpoint \
  --code samples/binary_search.py \
  --out results/deepseek-v3/binary_search.json
`
  Similarly, repeat these steps for each model:
      `python run_eval.py --model llama-3.1 --checkpoint /path/to/llama-3.1 ...
python run_eval.py --model gpt-oss-20b --checkpoint /path/to/gpt-oss-20b ...
`

run_eval.py should :
 1) load the model,
 2) feed the exact prompt and the student code,
 3) obtain the model response,
 4) post-process and save outputs as JSON



# Exact Prompt Used:

 You are an educational diagnostic assistant. Given a short Python function written by a student, produce:
  A. 1-2 Conceptual prompts that ask the student to explain a key concept used in their code (do not give the answer).
  B. 1-2 Misconception probes that point to potential incorrect assumptions, boundaries conditions, or inputs that may cause         failure.
  C. 1-2 Deeper-learning prompts that encourage the student to design tests, consider complexity trade-offs, or think about          robustness of the code (do not provide code fixes or final answers).

  Guidelines:
  - Always reference the relevant line(s) or variable(s) in the code.
  - Do not provide corrected code or step-by-step fixes.
  - Keep each prompt short (1–2 sentences), clear, and actionable for the student.
  - If appropriate, suggest specific test cases (e.g., empty list, target at first/last index, single element).

[Student python code]
   def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

numbers = [1, 3, 5, 7, 9, 11]
print(binary_search(numbers, 7))



# Reasoning





 






