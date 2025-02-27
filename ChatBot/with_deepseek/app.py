import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate,
)

# custom CSS styling

st.markdown(
    """
<style>
    /* Existing styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("DeepSeek Code Companion")
st.caption("Your AI Pair Programming Assistant")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        "Choose a model", ["deepseek-r1:1.5b", "deepseek-r1:3b", "deepseek-r1:7b"], index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown(
        """
    - **Code Generation**: Generate code snippets and entire functions.
    - **Code Review**: Review and suggest improvements to existing code.
    - **Code Refactoring**: Refactor code to improve readability and performance.
    - **Code Explanation**: Explain code to help you understand it better.
    """
    )

    st.divider()
    st.markdown(
        "Built with [Ollama](https://ollama.ai/) and [Langchain](https://python.langchain.com/docs/"
    )

# initiate the chat engine

llm_engine = ChatOllama(
    model=selected_model, base_url="http://localhost:11434", temperature=0.5
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a expert AI coding assistant. Provide concise, correct solution"
    "with strategic print statement for debugging. Always respond in English."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {
            "role": "ai",
            "content": "Hi! I'm DeepSeek Code Companion. How can I help you today?",
        }
    ]

# chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
# chat input and processing
user_query = st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke()

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)


if user_query:
    # add user query to message log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
        
    # add AI response to message log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # rerun to update chat display
    st.rerun()
    
    
