# AL Science Chatbot

Chat-bot for the A Level students to assist them in studies for the following subjects.

- Biology
- Chemistry
- Physics
<br>

## Overview

GPT 3.5 is Fine-tuned to identify the subject for the complex question asked by student and get a one word response of 'biology' or 'chemistry' or 'physics'.

- Notebook - [Fine-tune GPT-3.5](./notebooks/Fine_Tune_GPT_3_5_for_Vector_DB_Routing.ipynb)

Then by using it route the RAG pipeline the the specicfic vector database of that subject.

## Setup

### API keys
We'll be using [OpenAI](https://platform.openai.com/docs/models/) to access ChatGPT model `gpt-3.5-turbo`. Be sure to create your account and have your credentials ready.

### Repository
```bash
git clone https://github.com/shrikarsan/AL-Science-Chatbot.git
git config --global user.name <GITHUB-USERNAME>
git config --global user.email <EMAIL-ADDRESS>
```
### Environment

Then set up the environment correctly by specifying the values in your `.env` file,
and installing the dependencies:

```bash
pip install --user -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$PWD
```

### Credentials
```bash
touch .env

# Add environment variables to .env
OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY=""  # https://platform.openai.com/account/api-keys

source .env
```

### Config

Update paths for vector databases and finetuned model in [src/config](./src/config.py)

## Run

```bash
cd src && uvicorn main:app --host 0.0.0.0 --port 8000
```