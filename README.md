# Hotel Booking Data Analysis

## Project Overview

This project provides a comprehensive analysis of hotel booking data using advanced machine learning techniques. It employs sentence embeddings to process booking information and leverages Pinecone for efficient storage and retrieval of these embeddings. The analysis reveals valuable insights into booking trends and patterns, enabling stakeholders to make data-driven decisions.

## Features

- **Machine Learning Analysis**: Utilizes sentence embeddings for processing natural language booking data
- **Efficient Data Storage**: Integrates with Pinecone for optimized embedding storage and retrieval
- **Interactive Dashboard**: Streamlit-based user interface for exploring booking insights
- **FastAPI Backend**: Robust API endpoints for data processing and retrieval
- **Comprehensive Documentation**: Detailed notebooks explaining the analysis process

## Installation

To install the required libraries:

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with the following variables:

```
PINECONE_API_KEY=your_pinecone_api_key
```

Replace `your_pinecone_api_key` with your actual Pinecone API key.

## Usage

1. Configure environment variables in the `.env` file as described above.
2. Start the FastAPI backend:

```bash
uvicorn app:app --reload
```

3. Launch the Streamlit dashboard in a new terminal:

```bash
streamlit run app.py
```

4. Access the application in your web browser at `http://localhost:8501`.

## Project Structure

```
Booking-Data-Analysis/
├── app.py                  # Main application file for running the Streamlit app
├── embed_dataset.py        # Script for embedding the dataset
├── main.py                 # Main logic for data processing and analysis
├── requirements.txt        # List of required Python packages
├── README.md               # Project documentation
├── .env                    # Environment variables
├── config/                 # Configuration files
│   ├── __init__.py
│   ├── agents.py           # Agent configurations
│   └── tasks.py            # Task configurations
├── datasets/               # Directory containing datasets
│   ├── cleaned_booking_data.csv
│   └── hotel_bookings.csv
├── notebooks/              # Jupyter notebooks for analysis and reporting
│   ├── analytic_reporting.ipynb
│   └── preprocessing_dataset.ipynb
├── sample_test_queries.md  # Sample test queries and expected answers
└── implementation_report.md  # Report on implementation choices and challenges
```

## Crewai Agent workflow Diagram
![Image](https://github.com/user-attachments/assets/835a7044-1fbe-4686-9496-ffb8bc46d496)

## Demo Video Streamlit GUI Intergrated with Fastapi Backend
https://github.com/user-attachments/assets/e84bd366-8081-4bdc-a25c-ef81f100c593

## Repository Setup Instructions

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/Abhi-vish/BookingBrain.git
   ```

2. **Navigate to the Directory**:
   ```bash
   cd BookingBrain
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your Pinecone API key:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the Application**:
   - Start the FastAPI backend:
     ```bash
     uvicorn app:app --reload
     ```
   - Launch the Streamlit dashboard:
     ```bash
     streamlit run app.py
     ```

6. **Access the Application**: Open your web browser and navigate to `http://localhost:8501`.

## Implementation Details

### Technology Stack
- **Python**: Primary programming language for data processing and analysis
- **Streamlit**: Web application framework for interactive visualizations
- **Pinecone**: Vector database for efficient embedding storage and similarity search
- **FastAPI**: Backend framework for API development
- **Sentence Transformers**: For generating embeddings from natural language data

### Data Processing
- The project uses sentence embeddings to convert textual booking information into vector representations
- Data cleaning and preprocessing ensure high-quality input for analysis
- Pinecone indexes enable efficient similarity searches across large datasets

### Challenges and Solutions
- **Data Quality**: Implemented robust cleaning procedures to handle missing values and normalize data formats
- **Model Performance**: Experimented with various embedding models to optimize performance
- **Deployment**: Created a comprehensive environment configuration process for smooth setup

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for suggestions and improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.