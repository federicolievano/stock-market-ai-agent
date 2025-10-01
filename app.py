import streamlit as st
import os
from stock_agent import StockMarketAgent

def load_env_file():
    """Load environment variables from .env file or Streamlit secrets"""
    env_vars = {}
    
    # Try to load from Streamlit secrets first (for production)
    try:
        if hasattr(st, 'secrets') and st.secrets:
            env_vars.update(st.secrets)
    except:
        pass
    
    # Try to load from .env file (for local development)
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.lstrip('\ufeff')
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    
    return env_vars

# Page configuration
st.set_page_config(
    page_title="Stock Market AI Agent",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #ff6b6b;
    }
    .agent-message {
        background-color: #e8f4fd;
        border-left-color: #1f77b4;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)

def initialize_agent():
    """Initialize the Stock Market Agent"""
    env_vars = load_env_file()
    groq_api_key = env_vars.get("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("⚠️ Please set your GROQ_API_KEY in the environment variables or .env file")
        st.info("You can get a free API key from https://console.groq.com/")
        return None
    
    try:
        agent = StockMarketAgent(groq_api_key)
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Market AI Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.header("🤖 AI Agent Capabilities")
        st.markdown("""
        **Stock Market Information:**
        - Real-time stock prices
        - Historical data analysis
        - Market cap, volume, 52-week highs/lows
        - Cryptocurrency prices
        
        **Mathematical Operations:**
        - Basic calculations
        - Advanced math functions
        - Percentage calculations
        
        **Web Search:**
        - DuckDuckGo integration
        - Real-time information lookup
        """)
        
        st.header("💡 Example Questions")
        st.markdown("""
        - "What's the current price of Apple stock?"
        - "What was Bitcoin's price yesterday?"
        - "Calculate the average price of Tesla over the last week"
        - "What's 15% of 250?"
        - "Search for latest Tesla news"
        """)
        
        # API Key status
        env_vars = load_env_file()
        groq_api_key = env_vars.get("GROQ_API_KEY")
        if groq_api_key:
            st.success("✅ GROQ API Key configured")
        else:
            st.error("❌ GROQ API Key not configured")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = initialize_agent()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about stocks, crypto, or math!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        if st.session_state.agent:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.agent.chat(prompt)
                        st.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            error_msg = "Please configure your GROQ API key to use the agent."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Powered by Groq, LangChain, yfinance, and Streamlit</p>
        <p>Built with ❤️ for stock market enthusiasts</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
