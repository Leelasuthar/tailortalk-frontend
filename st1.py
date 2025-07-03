import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Calendar Booking Agent",
    page_icon="📅",
    layout="wide"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"  # Change for production

def send_message(message: str):
    """Send message to backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"content": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("📅 Calendar Booking Agent")
    st.write("I can help you book appointments, check availability, and suggest available times!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to do?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with example queries
    with st.sidebar:
        st.header("Example Queries")
        examples = [
            "Book an appointment for tomorrow at 2 PM",
            "Check if Monday at 10 AM is available",
            "What times are available on Friday?",
            "Schedule a meeting with John for next week"
        ]
        
        for example in examples:
            if st.button(example):
                st.session_state.messages.append({"role": "user", "content": example})
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = send_message(example)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

if __name__ == "__main__":
    main()