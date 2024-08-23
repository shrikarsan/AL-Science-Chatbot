from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from config import BIOLOGY_DB_PATH, CHEMISTRY_DB_PATH, PHYSICS_DB_PATH, FINETUNED_LLM

# Load Environmental Variables
load_dotenv()

# Data model
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["biology", "chemistry", "physics"] = Field(
        ...,
        description="Given a user question choose which datasource would be most relevant for answering their question",
    )

# LLM with function call 
route_llm = ChatOpenAI(model=FINETUNED_LLM)
structured_llm = route_llm.with_structured_output(RouteQuery)

# Prompt 
system = """Given a complex paragraph of AS & A Level science question, you will identify and output the relevant subject as 'biology', 'chemistry', or 'physics'."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

# Define router 
router = prompt | structured_llm

biology_vectordb = Chroma(persist_directory=BIOLOGY_DB_PATH, embedding_function=OpenAIEmbeddings())
biology_retriever = biology_vectordb.as_retriever()

chemistry_vectordb = Chroma(persist_directory=CHEMISTRY_DB_PATH, embedding_function=OpenAIEmbeddings())
chemistry_retriever = chemistry_vectordb.as_retriever()

physics_vectordb = Chroma(persist_directory=PHYSICS_DB_PATH, embedding_function=OpenAIEmbeddings())
physics_retriever = physics_vectordb.as_retriever()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

biology_chain = (
    {"context": biology_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

chemistry_chain = (
    {"context": chemistry_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

physics_chain = (
    {"context": physics_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def choose_route(result):
    if "biology" in result.datasource.lower():
        return biology_chain
    elif "chemistry" in result.datasource.lower():
        return chemistry_chain
    else:
        return physics_chain

    
full_chain = router | RunnableLambda(choose_route)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="AL Science Chatbot",
    description="Chat-bot for the A Level students to assist them in Biology, Chemistry, and Physics",
    lifespan=lifespan
)


@app.get("/query")
def query(query : str):
    try:
        output = full_chain.invoke({"question": query})
        return output
    except Exception as e:
        print(f"Error processing query: {e}")
        return {"error": "An error occurred while processing your query."}

            
if __name__ == "__main__":
    pass