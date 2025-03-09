## ---- unable to run this -----

# RAG application.
# Using vectorDB to store information contained in a PDF which is in a URL. 
# Retrieve the appropriate answers from the VectorDB using the Agent.


# There are 2 ways to run the Vector DB. 
# 1) via docker - local.  2) via AWS, AZURE, etc
# In this we will use docker file to read a PDF document.


# VectorDB
# Converting & Storing & Using 
# Create a Vector DB in Docker. 
# The content from the pdf will be extracted and stored in the Vector DB
# That content will be used to give accurate results based on the input search.


# import packages 
# import env variables
import typer
from typing import Optional,List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
from dotenv import load_dotenv
import os
load_dotenv() 

# use API keys to access the model
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


# Step-1
# Create the VectorDB using docker commands
# Keep the docker desktop open and running
# Run the following line in the vs code terminal - Git Bash by pasting all at once
# docker run -d \
#   -e POSTGRES_DB=ai \
#   -e POSTGRES_USER=ai \
#   -e POSTGRES_PASSWORD=ai \
#   -e PGDATA=/var/lib/postgresql/data/pgdata \
#   -v pgvolume:/var/lib/postgresql/data \
#   -p 5532:5432 \
#   --name pgvector \
#   phidata/pgvector:16
# pgvector image will be downloaded and Container would be running.


# Step-2
# PDF URL: https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai" # VectorDB running via Docker.
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(table_name="recipes", db_url=db_url)
)

knowledge_base.load()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    knowledge=knowledge_base,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=True,
    markdown=True,
    # debug_mode=True,
)
agent.print_response("How do I make chicken and galangal in coconut milk soup", stream=True)
agent.print_response("What was my last question?", stream=True)




