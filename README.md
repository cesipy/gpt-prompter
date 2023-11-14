# GPT-Prompter

This is a CLI tool to interact with openai's API.

## Installation

To run the python program you need an openai API key stored in the environment variable `OPENAI_API_KEY`.

To install all the necessary packages to use this GPT-Prompter you type:

```bash
pip install -r requirements.txt
```

## Usage

In order to interact with the API you can use various arguments. 

The default is using 'gpt3.5-turbo' model: 

```Python
python main.py
```

The model can be explicitly set using:

```python
python main.py <model-flag>
```

available model flags:

- --gpt3 for gpt3.5-turbo
- --gpt4 for gpt4
- --gpt3-16k for gpt3.5-turbo-16k
- --gpt4-32k for gpt4-32k
- --follow-up for follow up questions