import streamlit as st 
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv
load_dotenv()
 

os.environ["OPENAI_API_KEY"]= os.getenv("OPEN_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
## langsmith Tracking 
os.environ["LANGCHAIN_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]= "true"
os.environ["LANGCHAIN_PROJECT"]="Q&A Chatbot with OPENAI"
os.environ["OPENAI_MODEL_NAME"]="openai/gpt-oss-20b:free"

import os
import requests
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.tools import StructuredTool

# Load environment
load_dotenv()

# --- Tools that call your Backend API ---
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

def get_current_visitors() -> str:
    """Fetches the current number of visitors in the store."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/visitors/current")
        data = response.json()
        count = data.get("current_visitors", "N/A")
        return f"There are currently {count} visitors in the store."
    except Exception as e:
        return f"Sorry, I couldn't fetch the visitor count. Error: {e}"

def get_busiest_section() -> str:
    """Finds which store section has the most visitors."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/visitors/sections")
        sections = response.json()
        if sections:
            busiest = sections[0]  # Assuming sorted by traffic
            return f"The busiest section is '{busiest['section']}' with approximately {busiest['total_visitors']} visitors recently."
        return "I couldn't find any section data at the moment."
    except Exception as e:
        return f"Sorry, I couldn't find the busiest section. Error: {e}"

def get_cashier_queue() -> str:
    """Gets the current cashier queue status and wait time."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/cashier/current")
        status = response.json()
        if 'queue_length' in status:
            wait = status.get('wait_time_minutes', status['queue_length'] * 2)
            return f"The cashier queue has {status['queue_length']} people. Estimated wait time is {wait} minutes."
        return "Cashier status is currently unavailable."
    except Exception as e:
        return f"Sorry, I couldn't get cashier status. Error: {e}"

# --- Define Tools for LangChain ---
tools = [
    StructuredTool.from_function(get_current_visitors),
    StructuredTool.from_function(get_busiest_section),
    StructuredTool.from_function(get_cashier_queue),
]

# --- Create the Agent with Memory ---
llm = ChatOpenAI(model="amazon/nova-2-lite-v1:free", temperature=0, openai_api_key=os.getenv("OPEN_API_KEY"))
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    agent_kwargs=agent_kwargs,
    handle_parsing_errors=True
)

# --- Main Chat Loop ---
if __name__ == "__main__":
    print("🤖 Retail Analytics Bot is ready! (Type 'quit' to exit)")
    while True:
        try:
            query = input("\nYou: ")
            if query.lower() in ['quit', 'exit']:
                break
            response = agent.run(query)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Bot: Sorry, I encountered an error. Please try again.")