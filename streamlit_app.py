import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Get backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Default to localhost if not set

# Page config
st.set_page_config(
    page_title="CalendarAI - Smart Booking Assistant",
    page_icon="🤖",
    layout="wide"
)


# Simple CSS for clean styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Message styling */
    .user-message {
        background: #2563eb;
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.5rem 0;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: #f1f5f9;
        color: #1e293b;
        padding: 1rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 3px solid #06b6d4;
    }
    
    /* Button styling */
    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: background 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #1d4ed8;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }
    
    .sidebar-header {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    /* Status indicator */
    .status-online {
        color: #10b981;
        font-weight: 500;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: 500;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    </style>
    """, unsafe_allow_html=True)

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
        return f"⚠️ Connection Error: {str(e)}\n\nPlease make sure the backend server is running on {BACKEND_URL}"

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 CalendarAI</h1>
        <p>Your intelligent booking assistant</p>
    </div>
    """, unsafe_allow_html=True)

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def display_chat_message(message: Dict, is_user: bool = True):
    """Display a chat message"""
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 CalendarAI:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

def display_quick_actions():
    """Display quick action buttons"""
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-header">📚 Quick Actions</div>
    </div>
    """, unsafe_allow_html=True)
    
    quick_actions = [
        "Book appointment for tomorrow at 2 PM",
        "Check availability for Monday morning",
        "Suggest available times for this week",
        "Schedule team meeting for Friday",
        "Book doctor appointment next week"
    ]
    
    for i, action in enumerate(quick_actions):
        if st.button(action, key=f"quick_{i}"):
            return action
    return None

def display_features():
    """Display feature list"""
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-header">✨ Features</div>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        "Smart Intent Recognition",
        "Real-time Calendar Sync",
        "Natural Language Processing",
        "Instant Booking Confirmation",
        "Automatic Scheduling"
    ]
    
    for feature in features:
        st.markdown(f"• {feature}")

def main():
    # Load custom CSS
    load_custom_css()
    
    # Display header
    display_header()
    
    # Check backend status
    is_online = check_backend_status()
    if is_online:
        st.markdown('<div class="status-online">🟢 System Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">🔴 System Offline</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💬 Chat")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "👋 Welcome to CalendarAI! I can help you:\n\n• Book appointments and meetings\n• Check calendar availability\n• Suggest optimal time slots\n• Manage your schedule efficiently\n\nWhat would you like to do today?"
            })
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    display_chat_message(message, is_user=True)
                else:
                    display_chat_message(message, is_user=False)
        
        # Chat input
        st.markdown("---")
        
        # Input form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message...",
                placeholder="e.g., 'Book a meeting tomorrow at 3 PM'"
            )
            
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                send_button = st.form_submit_button("Send Message 📤", type="primary")
            
            with col_clear:
                if st.form_submit_button("Clear Chat 🗑️"):
                    st.session_state.messages = []
                    st.rerun()
        
        # Handle user input
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Show loading
            with st.spinner("🤖 CalendarAI is thinking..."):
                response = send_message(user_input)
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update chat
            st.rerun()
    
    with col2:
        # Sidebar content
        st.markdown("### 🎯 Quick Actions")
        quick_action = display_quick_actions()
        
        if quick_action:
            # Add quick action as user message
            st.session_state.messages.append({"role": "user", "content": quick_action})
            
            # Get response
            with st.spinner("🤖 Processing..."):
                response = send_message(quick_action)
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # st.markdown("---")
        
        # # Features
        # st.markdown("### ✨ Features")
        # display_features()
        
        # st.markdown("---")
        
        # Support section
        # st.markdown("""
        # <div class="sidebar-section">
        #     <div class="sidebar-header">🔧 Support</div>
        #     <p style="font-size: 0.9rem; color: #6b7280;">
        #         Need help? Contact our support team.
        #     </p>
        # </div>
        # """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()