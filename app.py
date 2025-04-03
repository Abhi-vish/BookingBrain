from fastapi import FastAPI
from pydantic import BaseModel
import json
from crewai import Crew, Process
from config.agents import BookingQueryAgent
from config.tasks import BookingQueryTask
from crewai import Agent, LLM
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer  # Import Hugging Face model
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

api_key =os.getenv('PINECONE_API_KEY')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
llm = LLM("gemini/gemini-1.5-flash")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
pinecone = Pinecone(
        api_key=api_key
    )

def query_resolver(query, context):
    agent = BookingQueryAgent().booking_query_agent(llm)
    task = BookingQueryTask().booking_query_task(agent, query, context)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=False,
        verbose=True
    )
    result = crew.kickoff()
    return result

def retrieve_embedding(query,top_k=10):
    # Connect to the index
    index_name = "booking-data"
    index = pinecone.Index(index_name)
    
    # Generate embedding for the query using your SentenceTransformer model
    query_embedding = embedding_model.encode(query).tolist()
    

    res = index.query(vector=[query_embedding],top_k=top_k, include_metadata=True)
    matched_data = []
    for match in res['matches']:
        matched_data.append(match['metadata']['text'])
        print(match['metadata']['text'])
    return matched_data

@app.post("/analytic_report")
async def create_analytic_report(report: dict):
    with open("analytic_report.json", "r") as file:
        analytic_report = json.load(file)
    return analytic_report


class BookingQuery(BaseModel):
    query:str

@app.post("/booking_query")
async def create_booking_query(data:BookingQuery):
    query = data.query
    context = retrieve_embedding(query)
    if context:
        result = query_resolver(query,context)
        return result.raw
    else:
        raise ValueError("No context found for the query.")
