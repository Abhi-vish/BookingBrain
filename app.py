from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import streamlit as st

from pinecone import Pinecone, ServerlessSpec
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

# Load pre-trained embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API'))
index_name = "booking-data"

# Load the dataset
df = pd.read_csv('datasets/cleaned_booking_data.csv')

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


# Generate embeddings for the text data
embeddings = embedding_model.encode(df["text"].tolist()).tolist()

if index_name not in Pinecone.list_indexes():
    pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

index = Pinecone.Index(index_name)

if embeddings:
    # Prepare vectors with metadata
    vectors = [
        (str(uuid.uuid4()), emb, {"text": text})
        for text, emb in zip(df["text"], embeddings)
    ]

    # Upsert vectors into Pinecone
    index.upsert(vectors)

else:
    st.write("No embeddings to upsert.")