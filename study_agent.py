import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool


# --------------------------------------------------
# 1. Gemini API Key
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")


# --------------------------------------------------
# 2. Gemini Model
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# 3. Study Topics Tool
# --------------------------------------------------

@tool
def get_available_topics() -> str:
    """
    Returns the subjects and topics currently available for study.
    """

    topics = {
        "DBMS": [
            "Normalization",
            "Transactions",
            "Indexing",
            "SQL Joins"
        ],
        "Java": [
            "OOP",
            "Inheritance",
            "Interfaces",
            "Exception Handling"
        ],
        "Machine Learning": [
            "Regression",
            "Classification",
            "Evaluation Metrics",
            "Decision Trees"
        ],
        "Cloud Computing": [
            "Virtualization",
            "Cloud Service Models",
            "CAPEX vs OPEX",
            "Distributed Computing"
        ]
    }

    result = []

    for subject, subject_topics in topics.items():
        result.append(
            f"{subject}: " + ", ".join(subject_topics)
        )

    return "\n".join(result)


# --------------------------------------------------
# 4. Study Planner Agent
# --------------------------------------------------

study_agent = create_agent(
    model=llm,
    tools=[get_available_topics],
    system_prompt="""
You are a helpful Study Planner Agent.

Your job is to create realistic study plans for students.

Rules:

1. Understand the student's available study time.
2. Understand which subjects they want to study.
3. Use the get_available_topics tool when you need
   to know what topics are available.
4. Divide study time into focused sessions.
5. Include short breaks when appropriate.
6. Prioritize important topics.
7. Do not create an unrealistic schedule.
8. Keep the final plan clear and easy to follow.

Format the final answer as:

📚 Study Plan

⏰ Time:
📖 Subject:
🎯 Topic:
⏱️ Duration:

Include a short reason for the prioritization.
"""
)


# --------------------------------------------------
# 5. Function used by FastAPI
# --------------------------------------------------

def generate_study_plan(user_request: str) -> str:

    response = study_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_request
            }
        ]
    })

    return response["messages"][-1].content