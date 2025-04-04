import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Booking Analytics & QA System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the API endpoints
API_URL = "http://localhost:8000"  # Change this to your FastAPI server URL
ANALYTICS_ENDPOINT = f"{API_URL}/analytics"
QUERY_ENDPOINT = f"{API_URL}/ask"

# Function to fetch analytics data
def get_analytics_data():
    try:
        response = requests.post(ANALYTICS_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching analytics data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Exception while fetching analytics data: {e}")
        return None

# Function to send query to the API
def send_query(query_text):
    try:
        response = requests.post(QUERY_ENDPOINT, json={"query": query_text})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error processing query: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Exception while processing query: {e}")
        return None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0D47A1;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
        margin-bottom: 20px;
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f8ff;
        margin: 5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #616161;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<div class='main-header'>🏨 Booking Analytics</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Query System", "About"])

if page == "Dashboard":
    st.markdown("<div class='main-header'>Booking Analytics Dashboard</div>", unsafe_allow_html=True)
    st.write("Welcome to the Booking Analytics Dashboard. This interface provides insights into hotel booking data.")
    
    # Fetch analytics data
    analytics_data = get_analytics_data()
    
    if analytics_data:
        # Display Key Metrics
        st.markdown("<div class='sub-header'>Key Metrics</div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{analytics_data['overview']['total_bookings']}</div>
                <div class='metric-label'>Total Bookings</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{analytics_data['overview']['cancellation_rate']}</div>
                <div class='metric-label'>Cancellation Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>${analytics_data['overview']['total_revenue']:.2f}</div>
                <div class='metric-label'>Total Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{analytics_data['revenue_trends']['peak_month']}</div>
                <div class='metric-label'>Peak Revenue Month</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display Revenue Trends
        st.markdown("<div class='sub-header'>Revenue Trends</div>", unsafe_allow_html=True)
        revenue_data = pd.DataFrame(
            list(analytics_data['revenue_trends']['monthly_revenue'].items()),
            columns=['Month', 'Revenue']
        )
        fig = px.line(
            revenue_data, 
            x='Month', 
            y='Revenue', 
            title='Monthly Revenue Trends',
            labels={'Month': 'Month', 'Revenue': 'Revenue ($)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display Geographical Distribution
        st.markdown("<div class='sub-header'>Geographical Distribution</div>", unsafe_allow_html=True)
        geo_data = pd.DataFrame(
            list(analytics_data['geographical_distribution']['top_booking_countries'].items()),
            columns=['Country', 'Bookings']
        )
        fig = px.bar(
            geo_data,
            x='Country',
            y='Bookings',
            color='Bookings',
            title='Top Booking Countries',
            labels={'Country': 'Country', 'Bookings': 'Number of Bookings'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display Cancellation Rate by Hotel Type
        st.markdown("<div class='sub-header'>Cancellation Analysis</div>", unsafe_allow_html=True)
        cancel_data = pd.DataFrame(
            list(analytics_data['cancellation_analysis']['cancellation_by_hotel_type'].items()),
            columns=['Hotel Type', 'Cancellation Rate']
        )
        fig = px.pie(
            cancel_data, 
            values='Cancellation Rate', 
            names='Hotel Type',
            title='Cancellation Rate by Hotel Type'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Unable to fetch analytics data. Please check if the API server is running.")

elif page == "Query System":
    st.markdown("<div class='main-header'>Booking Query System</div>", unsafe_allow_html=True)
    st.write("Ask questions about the booking data and get AI-powered answers.")
    
    # Create a list of example queries
    example_queries = [
        "Show me total revenue for July 2017.",
        "Which locations had the highest booking cancellations?",
        "What is the average price of a hotel booking?",
        "What is the most common customer type?",
        "How does the cancellation rate vary by month?"
    ]
    
    # Add examples
    st.markdown("<div class='sub-header'>Example Questions</div>", unsafe_allow_html=True)
    selected_example = st.selectbox("Select an example query:", [""] + example_queries)
    
    # Query input
    query_input = st.text_area("Enter your question:", value=selected_example, height=100)
    
    # Submit button
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.button("Submit Query", use_container_width=True)
    
    # Display query history
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    # Process query
    if submit_button and query_input:
        with st.spinner("Processing your query..."):
            # Add query to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Send query to API
            response = send_query(query_input)
            
            if response:
                # Add to history
                st.session_state.query_history.append({
                    "timestamp": timestamp,
                    "query": query_input,
                    "response": response
                })
                
                # Display the result
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='sub-header'>Response</div>", unsafe_allow_html=True)
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Failed to get a response. Please try again.")
    
    # Display query history
    if st.session_state.query_history:
        st.markdown("<div class='sub-header'>Query History</div>", unsafe_allow_html=True)
        
        for i, item in enumerate(reversed(st.session_state.query_history)):
            with st.expander(f"Query at {item['timestamp']}: {item['query'][:50]}{'...' if len(item['query']) > 50 else ''}"):
                st.write("**Question:**")
                st.write(item['query'])
                st.write("**Answer:**")
                st.write(item['response'])

elif page == "About":
    st.markdown("<div class='main-header'>About This System</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <div class='sub-header'>LLM-Powered Booking Analytics & QA System</div>
        <p>This system processes hotel booking data, extracts insights, and enables retrieval-augmented question answering (RAG).</p>
        
        <div class='sub-header'>Key Components</div>
        <ul>
            <li><strong>Analytics Dashboard:</strong> Visualizes booking data, revenue trends, geographical distribution, and more.</li>
            <li><strong>RAG-based Query System:</strong> Uses vector embeddings and LLM to answer natural language questions about booking data.</li>
            <li><strong>Interactive Interface:</strong> User-friendly Streamlit interface for exploring data and asking questions.</li>
        </ul>
        
        <div class='sub-header'>Technologies Used</div>
        <ul>
            <li><strong>Backend:</strong> FastAPI for API endpoints</li>
            <li><strong>AI:</strong> Gemini 1.5 Flash LLM with CrewAI framework</li>
            <li><strong>Vector Database:</strong> Pinecone for storing embeddings</li>
            <li><strong>Embeddings:</strong> SentenceTransformer for generating embeddings</li>
            <li><strong>Frontend:</strong> Streamlit for interactive visualization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 Booking Analytics & QA System")