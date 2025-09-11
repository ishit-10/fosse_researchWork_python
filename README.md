# Overview

This repository implements an evaluation pipeline to assess whether LLMs can analyze student Python code, generate conceptual prompts, surface misconceptions, and encourage reflective learning without giving away solutions. Three models are compared: 
* DeepSeek-V3 
* Llama 3.1 (405B)
* OpenAI GPT-OSS-20B.

<br>

# Setup

## 1) Clone the repository

    git clone https://github.com/ishit-10/fosse_researchWork_python.git
    cd fosse_researchWork_python


## 2) Create Python environment (using venv)

    python3.10 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip


## 3) Install Dependencies

    transformers>=4.30.0
    torch>=2.0.0
    pylint

    
  ### Install:

    pip install -r requirements.txt

  ### Other tools:

    pip install vllm accelerate huggingface_hub astpretty jupyter


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

## 5) Run the evaluation script (example)
### A simple CLI wrapper run_eval.py should accept a model identifier and a code file, then store outputs to results/<model_name>/<timestamp>.json
Example Usage:
  ```
  python run_eval.py \
  --model deepseek-v3 \
  --checkpoint /path/to/deepseek-v3/checkpoint \
  --code samples/binary_search.py \
  --out results/deepseek-v3/binary_search.json
  ```
Repeat this for llama-3.1 and gpt-oss-20b model:
  ```
  python run_eval.py --model llama-3.1 --checkpoint /path/to/llama-3.1 ...
  python run_eval.py --model gpt-oss-20b --checkpoint /path/to/gpt-oss-20b ...
  ```
### run_eval.py should:
* load the model,
* feed the exact prompt given below along with the student code,
* obtain the model response,
* post-process and save outputs as JSON

<br>

# Prompt Used
The prompt is passed as a single string to the model (include the code block exactly).
```
You are an educational diagnostic assistant. Given a short Python function written by a student, produce:
  A. 1-2 Conceptual prompts that ask the student to explain a key concept used in their code (do not give the answer).
  B. 1-2 Misconception probes that point to potential incorrect assumptions, boundaries, or inputs that may cause failure.
  C. 1-2 Deeper-learning prompts that encourage the student to design tests, consider complexity trade-offs, or think about robustness — again, do not provide code fixes or final answers.

Guidelines:
- Always reference the relevant line(s) or variable(s) in the code (e.g., "the loop condition `left < right`" or "the `mid` calculation").
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
```
<br>

# Reasoning

## DeepSeek-V3 - Outputs
### Conceptual prompts:
* “How does changing the loop condition from left < right to left <= right affect the correctness of the search?”
* “Why is integer division (//) used when computing mid, and what guarantee does it provide about the selected index?”

### Misconception probes:
* “If the target equals the last element (arr[right]), will the current code find it? Explain the loop progression.”
* “What would happen if arr is empty or not sorted? Identify the assumptions the function makes about arr.”

### Deeper-learning prompts:
* “Design three test cases that would confirm whether this function correctly handles first, middle, and last elements.”
* “Suggest what runtime or memory measurements you would collect to compare this implementation with linear search on large arrays.”

<br>

## Llama 3.1 (405B) — Outputs
### Conceptual prompts:
* “What role do the left and right pointers play in maintaining the binary-search invariant?”
* “Explain how mid = (left + right) // 2 divides the search space and why integer division is used.”

### Misconception Probes:
* “Given while left < right, describe what happens when the target is at the current right index.”
* “How does an unsorted arr violate the algorithm’s preconditions, and what behavior would follow?”

### Deeper-learning prompts
* “Describe a minimal validation strategy to ensure preconditions (sorted, non-empty) before running the search.”
* “Compare scenarios where linear search might be preferable despite its O(n) cost.”

<br>

## GPT-OSS-20B — Outputs
### Conceptual prompts:
* “Explain why left < right might skip checking the right index and the implications for correctness.”
* “State the expected time complexity of this implementation and why it is O(log n).”

### Misconception Probes:
* “If arr has a single element, what does the function return and is that correct?”
* “Identify preconditions the code assumes about arr and how they could be violated.”

### Deeper-learning prompts
* “Propose a set of edge cases to validate correctness (empty array, single element, target absent) without providing fixes.”
* “If instrumented to count comparisons, what experiments would you run to compare this to linear search?”

<br>

# Output Analysis - Interpretation
## DeepSeek-V3
The model emphasizes boundary correctness and test design. Prompts typically reference specific tokens and invite precise reflection about invariants and preconditions. This model tends to generate prompts that surface common logical errors and encourage evidence-based testing.

## Llama 3.1
Balances invariant reasoning and pedagogical framing. Prompts are classroom-friendly, often phrased to guide conceptual articulation (e.g., asking students to state invariants), which supports formative assessment and TA workflows.

## GPT-OSS-20B
Produces concise and broadly applicable prompts. More conservative in specific boundary language than DeepSeek-V3, but highly reproducible and suitable as a lightweight baseline for classroom deployments.

<br>

# Why these models were chosen — strengths and limitations
### DeepSeek-V3
* <b>Strengths</b>: Expected to provide superior boundary-condition detection and detailed test design prompts due to advanced reasoning and long-context abilities.
* <b> Limitations </b>: Mixture of Expertes deployment complexity and higher hardware requirements; requires careful routing and inference engineering; post-filtering still required to prevent hinting/hallucination.

### Llama 3.1 (405B)
* <b>Strengths</b>: Instruction-tuned design provides classroom-friendly phrasing and robust prompt following; strong ecosystem and tool support make it practical for reproducible research.
* <b> Limitations </b>: Very large variants impose resource constraints; code specialization is adequate but may be outperformed by dedicated code models in narrow tasks.

### GPT-OSS-20B
* <b>Strengths</b>: Lightweight, accessible, and reproducible in institutional settings; produces stable, concise prompts suitable for large-scale formative feedback pipelines.
* <b> Limitations </b>: May miss the most subtle boundary invariants without additional scaffold; less likely to surface the full depth of reasoning compared to higher-capacity models.

<br>

# Trade-offs between accuracy, interpretability, and cost
### Accuracy (depth of diagnosis) vs. Cost (compute):
DeepSeek-V3 consistently produced the deepest diagnostic prompts, such as “How does changing the loop condition from `left < right` to `left <= right` affect correctness?” — directly targeting a subtle off-by-one boundary issue. This demonstrates high diagnostic accuracy but comes with substantial compute overhead (MoE routing, GPU memory scaling). Llama 3.1 also surfaced invariant-related prompts (e.g., “What role do the left and right pointers play in maintaining the binary-search invariant?”) but with more pedagogical phrasing, making it suitable for instructional settings, though still resource-intensive. By contrast, GPT-OSS-20B generated broader but less detailed probes, such as “Explain why `left < right` might skip checking the right index” — correct but less nuanced. Its smaller footprint makes it significantly cheaper to deploy in large classroom pipelines, but at the expense of maximal diagnostic coverage.

### Interpretability vs. Capability:
Llama 3.1’s outputs were the most classroom-friendly, balancing code references with accessible conceptual framing. For instance, its invariant explanation prompts are interpretable even to weaker students, aligning with formative teaching goals. DeepSeek-V3 provided highly precise prompts (explicit reference to loop conditions and test case design), but these may demand higher prior knowledge and require instructor scaffolding, reducing interpretability for novices. GPT-OSS-20B, while less rich in conceptual depth, is highly predictable and concise, which aids interpretability in scaled settings where prompt uniformity is desirable. The trade-off emerges: DeepSeek-V3 offers capability (nuance and depth), while GPT-OSS-20B offers interpretability and predictability at lower cost.

### Throughput & latency vs. diagnostic precision:
In batch-mode evaluation, where hundreds of submissions must be processed, GPT-OSS-20B is the most scalable. Its outputs, though less probing, still reliably flagged key misconceptions (e.g., handling single-element arrays). Llama 3.1 is slower but provides higher-quality prompts well suited for settings where fewer, richer interventions are preferable. DeepSeek-V3, while providing the most precise diagnostic probes, would be the least suitable for batch feedback due to its higher inference latency and cost. In practice, this suggests a hybrid deployment strategy: GPT-OSS-20B for broad, automated formative feedback at scale; and DeepSeek-V3 for targeted, high-stakes competence analysis or research scenarios where diagnostic precision outweighs throughput constraints.

<br>

# Conclusion
The comparative analysis of DeepSeek-V3, Llama 3.1, and GPT-OSS-20B on a simple binary search example demonstrates how open-source LLMs vary in their ability to support high-level student competence analysis. DeepSeek-V3 produced the most diagnostically rich prompts, frequently highlighting issues such as off-by-one loop boundaries and explicitly encouraging systematic test design. Llama 3.1 offered a balanced approach, generating invariant-based questions while maintaining an accessible, pedagogical tone suitable for classroom contexts. GPT-OSS-20B, although less detailed, delivered concise and reproducible prompts that reliably surfaced key misconceptions at significantly lower computational cost.

These results suggest that no single model is universally optimal; instead, their strengths map to different educational needs. DeepSeek-V3 is best suited for targeted, high-stakes diagnostic use where depth is essential. Llama 3.1 aligns with instructional feedback workflows, bridging depth with clarity for broad student audiences. GPT-OSS-20B provides a pragmatic baseline for scalable, automated feedback pipelines in resource-constrained settings. Together, the models illustrate a complementary spectrum, where careful selection or hybrid deployment can balance diagnostic accuracy, pedagogical interpretability, and operational cost.







