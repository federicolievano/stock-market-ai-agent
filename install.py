#!/usr/bin/env python3
"""
Installation script for Stock Market AI Agent
This script helps set up the environment and dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required packages"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        try:
            with open(".env", "w") as f:
                f.write("# Add your API keys here\n")
                f.write("GROQ_API_KEY=\n")
                f.write("ALPHA_VANTAGE_API_KEY=\n")
            print("✅ .env file created!")
            print("⚠️  Please edit .env and add your actual GROQ API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {str(e)}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    """Main installation process"""
    print("🚀 Stock Market AI Agent - Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed!")
        print("Please try installing dependencies manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get a free API key from https://console.groq.com/")
    print("2. Edit the .env file and add your GROQ_API_KEY")
    print("3. Run the test script: python test_agent.py")
    print("4. Start the app: streamlit run app.py")
    
    print("\n💡 Example .env content:")
    print("GROQ_API_KEY=your_groq_api_key")
    print("ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key")

if __name__ == "__main__":
    main()
