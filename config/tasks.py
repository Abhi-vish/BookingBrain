from crewai import Task
from textwrap import dedent

class BookingQueryTask:
    def booking_query_task(self, agent, question, context):
        return Task(
            description=dedent(f"""
                You are an expert Booking Analytics Assistant. Your goal is to accurately answer user queries based on provided booking data. 

                Instructions:
                - Use the given data context to derive an answer.
                - If the answer requires calculations (e.g., average price, cancellation rate), process the data accordingly.
                - If the data does not directly provide an answer, infer insights logically.
                - If the query is ambiguous, ask the user for clarification before responding.
                - Provide structured and well-explained responses, including figures, trends, or insights where relevant.

                Query: {question}
                Data Context: {context}     
            """),
            expected_output="""
                - A well-structured response that directly answers the query.
                - If calculations are needed, provide step-by-step reasoning.
                - Mention relevant trends, statistics, or patterns if applicable.
                - If the data is insufficient, politely inform the user and suggest alternative queries.
            """,
            agent=agent,
            verbose=True
        )
