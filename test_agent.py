#!/usr/bin/env python3
"""
Test script for the Stock Market AI Agent
Run this to verify the agent is working correctly
"""

import os
import sys

def load_env_file():
    """Load environment variables from .env file manually"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().lstrip('\ufeff')
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return env_vars

def test_agent():
    """Test the Stock Market Agent functionality"""
    
    # Load environment variables manually
    env_vars = load_env_file()
    groq_api_key = env_vars.get("GROQ_API_KEY")
    
    # Debug information
    print("Debug - env_vars:", env_vars)
    print("Debug - groq_api_key:", groq_api_key)
    
    if not groq_api_key:
        print("❌ GROQ_API_KEY not configured!")
        print("Please set your GROQ_API_KEY in the .env file")
        print("You can get a free API key from https://console.groq.com/")
        return False
    
    try:
        from stock_agent import StockMarketAgent
        
        print("🤖 Initializing Stock Market Agent...")
        try:
            agent = StockMarketAgent(groq_api_key)
            print("✅ Agent initialized successfully!")
        except Exception as init_error:
            print(f"❌ Error creating StockMarketAgent: {str(init_error)}")
            print(f"❌ Error type: {type(init_error).__name__}")
            return False
        
        # Test questions
        test_questions = [
            "What is 2 + 2?",
            "What's the current price of Apple stock?",
            "Calculate 15% of 250"
        ]
        
        print("\n🧪 Running test questions...")
        for i, question in enumerate(test_questions, 1):
            print(f"\n--- Test {i} ---")
            print(f"Q: {question}")
            
            try:
                response = agent.chat(question)
                print(f"A: {response}")
                print("✅ Test passed!")
            except Exception as e:
                print(f"❌ Test failed: {str(e)}")
                return False
        
        print("\n🎉 All tests passed! The agent is ready to use.")
        print("\nTo run the Streamlit app:")
        print("streamlit run app.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Please install all dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Stock Market AI Agent - Test Suite")
    print("=" * 50)
    
    success = test_agent()
    
    if success:
        print("\n✅ Setup complete! You can now run the Streamlit app.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
