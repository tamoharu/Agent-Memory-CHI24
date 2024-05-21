# "My agent understands me better": Integrating Dynamic Human-like Memory Recall and Consolidation in LLM-Based Agents

This project is a demonstration of a dialogue agent system that implements human-like memory processes, as described in the following research papers:
https://dl.acm.org/doi/fullHtml/10.1145/3613905.3650839
https://arxiv.org/abs/2404.00573

## Setup

1. Create a virtual environment:

```
python -m venv venv
```

2. Activate the virtual environment:

```
source venv/bin/activate  # For Unix/Linux
```
```
venv\Scripts\activate.bat  # For Windows
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Open the config/globals file and enter your name in the user field.

5. Open the config/prompts file and enter your custom prompts.

6. Running the Demo

```
python run.py
```