from crewai import Task
from textwrap import dedent

class BookingQueryTask:
    def booking_query_task(self, agent, question, context):
        return Task(
            description=dedent(f"""
                You are an expert Booking Analytics Assistant analyzing hotel booking data to answer user queries with precision.
                
                CONTEXT INFORMATION:
                {context}
                
                USER QUERY:
                {question}
                
                ANALYSIS INSTRUCTIONS:
                1. First, carefully identify what specific metrics, time periods, or segments the query is targeting
                2. Determine if the provided context contains all necessary data to answer the query
                3. For quantitative questions:
                   - Perform explicit calculations showing your work
                   - Round financial figures to 2 decimal places
                   - Express percentages with 1 decimal place
                   - Include sample size and time period analyzed
                4. For trend or pattern questions:
                   - Identify relevant variables in the data
                   - Note any seasonality or cyclical patterns
                   - Compare against industry benchmarks if available
                5. For geographical or demographic questions:
                   - Segment data appropriately
                   - Present a complete distribution when relevant
                   - Highlight significant differences between segments
                
                RESPONSE FORMAT:
                1. Begin with a direct, concise answer to the query
                2. Support with relevant metrics and calculations
                3. Provide context by comparing to averages or trends
                4. Include any important caveats about data limitations
                5. When appropriate, suggest actionable insights based on the findings
                
                ACCURACY REQUIREMENTS:
                - Cross-check calculations by using alternative methods when possible
                - Verify that date ranges in analysis match what was requested
                - Ensure consistency in units and currencies
                - Report confidence level in your answer based on data quality and completeness
                
                If the query cannot be answered with the available data:
                1. Explain specifically what information is missing
                2. Provide the closest available insights from the data
                3. Suggest how to refine the query to get an answerable question
            """),
            expected_output=dedent("""
                A comprehensive analytics response that includes:
                
                1. SUMMARY ANSWER:
                   - Direct response to the query in 1-2 sentences
                   
                2. DETAILED ANALYSIS:
                   - Relevant metrics with precise calculations
                   - Segmentation breakdown if applicable
                   - Clear methodology explanation
                   - Supporting evidence from the data
                   
                3. CONTEXTUAL INSIGHTS:
                   - Patterns, anomalies, or notable findings
                   - Comparison to broader trends when relevant
                   - Potential business implications
                   
                4. DATA LIMITATIONS:
                   - Explicit mention of any data constraints
                   - Confidence level in the provided answer
                   
                5. FOLLOW-UP SUGGESTIONS:
                   - Related metrics that might be valuable to explore
                   - Alternative ways to analyze this data point
            """),
            agent=agent,
            verbose=True
        )