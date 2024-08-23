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
