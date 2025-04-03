import pandas as pd
import numpy as np
import streamlit as st
from pinecone import Pinecone, ServerlessSpec
import uuid
from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time  # Import time module for sleep functionality
from sentence_transformers import SentenceTransformer  # Import Hugging Face model

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = "booking-data"

# Load the dataset
df = pd.read_csv('datasets/cleaned_booking_data.csv')

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# Generate text representations for each row
df["text"] = df.apply(lambda row: (
    f"Booking ID: {row.name}, "
    f"Hotel: {row['hotel']}, "
    f"Cancellation: {'Yes' if row['is_canceled'] == 1 else 'No'}, "
    f"Lead Time: {row['lead_time']} days, "
    f"Arrival: {row['arrival_date_day_of_month']} {row['arrival_date_month']} {row['arrival_date_year']}, "
    f"Week Number: {row['arrival_date_week_number']}, "
    f"Weekend Nights: {row['stays_in_weekend_nights']}, Week Nights: {row['stays_in_week_nights']}, "
    f"Guests: {row['adults']} adults, {row['children']} children, {row['babies']} babies, "
    f"Deposit: {row['deposit_type']}, "
    f"Agent: {row['agent'] if not pd.isna(row['agent']) else 'N/A'}, "
    f"Waiting List Days: {row['days_in_waiting_list']}, "
    f"Customer Type: {row['customer_type']}, "
    f"Price: {row['adr']} EUR, "
    f"Parking Spaces: {row['required_car_parking_spaces']}, "
    f"Special Requests: {row['total_of_special_requests']}, "
    f"Reservation Status: {row['reservation_status']} on {row['reservation_status_date']}."
), axis=1)

# Initialize Hugging Face model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Load the model

# Define chunk size for DataFrame
chunk_size = 100  # Adjust this value as needed
chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]  # Chunk the DataFrame

# Check if the index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

# Process each chunk
for chunk in chunks:
    # Generate embeddings for the chunk
    embeddings = embedding_model.encode(chunk["text"].tolist()).tolist()  # Generate embeddings

    # Prepare and upsert vectors with metadata
    vectors = [
        (str(uuid.uuid4()), emb, {"text": text})
        for text, emb in zip(chunk["text"], embeddings)
    ]

    # Upload vectors to Pinecone
    index.upsert(vectors)
    print(f"Uploaded chunk with {len(vectors)} embeddings.")
    time.sleep(72)  # Sleep for 1.2 minutes

st.write("Embeddings upserted successfully.")
