import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List

# Page config
st.set_page_config(
    page_title="CalendarAI Pro - Smart Booking Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"  # Change for production

# Custom CSS for enterprise styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --neutral-50: #f8fafc;
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-400: #94a3b8;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1);
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        margin-left: 3rem;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--neutral-800);
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        margin-right: 3rem;
        border-left: 4px solid var(--accent-color);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-header {
        color: var(--neutral-800);
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--neutral-100);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, #5855eb 0%, #7c3aed 100%);
    }
    
    .secondary-button {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        color: var(--neutral-700) !important;
        border: 1px solid var(--neutral-200) !important;
    }
    
    .secondary-button:hover {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid var(--neutral-200);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-color);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        color: var(--neutral-600);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Status indicators */
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: var(--success-color);
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-text {
        color: var(--success-color);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 3px solid var(--neutral-200);
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Quick actions */
    .quick-action {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        border: 1px solid var(--neutral-200);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-color);
    }
    
    .quick-action-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    .quick-action-text {
        font-weight: 500;
        color: var(--neutral-700);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .user-message,
        .assistant-message {
            margin-left: 1rem;
            margin-right: 1rem;
        }
    }
    
    /* Hide Streamlit elements */
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
        <h1>🤖 CalendarAI Pro</h1>
        <p>Your intelligent booking assistant powered by advanced AI</p>
    </div>
    """, unsafe_allow_html=True)

def display_status_indicator():
    """Display connection status"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <span class="status-online"></span>
                <span class="status-text">System Online</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Backend service unavailable")
    except:
        st.error("❌ Cannot connect to backend service")

def display_chat_message(message: Dict, is_user: bool = True):
    """Display a chat message with custom styling"""
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
    <div class="sidebar-content">
        <div class="sidebar-header">
            📚 Quick Actions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    quick_actions = [
        {"icon": "📅", "text": "Book appointment for tomorrow at 2 PM", "action": "book_tomorrow"},
        {"icon": "🔍", "text": "Check availability for Monday morning", "action": "check_monday"},
        {"icon": "💡", "text": "Suggest available times for this week", "action": "suggest_week"},
        {"icon": "📋", "text": "Schedule team meeting for Friday", "action": "team_meeting"},
        {"icon": "🏥", "text": "Book doctor appointment next week", "action": "doctor_appointment"},
        {"icon": "💼", "text": "Schedule client call tomorrow", "action": "client_call"}
    ]
    
    for action in quick_actions:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='font-size: 1.2rem; text-align: center;'>{action['icon']}</div>", unsafe_allow_html=True)
        with col2:
            if st.button(action['text'], key=action['action']):
                return action['text']
    return None

def display_usage_stats():
    """Display usage statistics"""
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header">
            📊 Today's Stats
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">12</div>
            <div class="metric-label">Appointments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">89%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)

def display_features():
    """Display feature highlights"""
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header">
            ✨ Features
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        "🎯 Smart Intent Recognition",
        "📅 Real-time Calendar Sync",
        "🤖 Natural Language Processing",
        "⚡ Instant Booking Confirmation",
        "🔄 Automatic Scheduling",
        "📱 Multi-platform Support"
    ]
    
    for feature in features:
        st.markdown(f"""
        <div style="padding: 0.5rem 0; color: var(--neutral-700);">
            {feature}
        </div>
        """, unsafe_allow_html=True)

def display_example_conversations():
    """Display example conversation starters"""
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-header">
            💬 Example Conversations
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    examples = [
        "I need to book a dentist appointment for next Tuesday",
        "What's my availability for client meetings this week?",
        "Can you schedule a 1-hour meeting with Sarah tomorrow?",
        "Block my calendar for vacation next month",
        "Find me 30 minutes for a phone call today"
    ]
    
    for i, example in enumerate(examples):
        with st.expander(f"Example {i+1}"):
            st.write(f"**You:** {example}")
            st.write("**CalendarAI:** I'll help you with that! Let me check your calendar availability...")

def main():
    # Load custom CSS
    load_custom_css()
    
    # Display header
    display_header()
    
    # Display status
    display_status_indicator()
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "👋 Welcome to CalendarAI Pro! I'm your intelligent booking assistant. I can help you:\n\n• Book appointments and meetings\n• Check calendar availability\n• Suggest optimal time slots\n• Manage your schedule efficiently\n\nWhat would you like to do today?"
            })
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                display_chat_message(message, is_user=True)
            else:
                display_chat_message(message, is_user=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        chat_container = st.container()
        with chat_container:
            user_input = st.text_input(
                "Type your message...",
                key="user_input",
                placeholder="e.g., 'Book a meeting tomorrow at 3 PM' or 'Check my availability for Friday'"
            )
            
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                send_button = st.button("Send Message 📤", type="primary")
            
            with col_clear:
                if st.button("Clear Chat 🗑️"):
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
            
            # Clear input and rerun
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
        
        st.markdown("---")
        
        # Usage stats
        st.markdown("### 📊 Statistics")
        display_usage_stats()
        
        st.markdown("---")
        
        # Features
        st.markdown("### ✨ Features")
        display_features()
        
        st.markdown("---")
        
        # Example conversations
        st.markdown("### 💬 Examples")
        display_example_conversations()
        
        st.markdown("---")
        
        # Support section
        st.markdown("""
        <div class="sidebar-content">
            <div class="sidebar-header">
                🔧 Support
            </div>
            <p style="font-size: 0.9rem; color: var(--neutral-600);">
                Need help? Contact our support team or check the documentation.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()