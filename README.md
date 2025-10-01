# Stock Market AI Agent

An intelligent conversational AI agent that provides real-time stock market information, cryptocurrency prices, and performs mathematical operations.

## Features

- 📈 **Real-time Stock Prices**: Get current prices for any stock symbol
- 💰 **Cryptocurrency Data**: Bitcoin, Ethereum, and other crypto prices  
- 📊 **Historical Analysis**: View historical data and calculate percentage changes
- 🧮 **Mathematical Operations**: Perform calculations and percentage operations
- 🔍 **Web Search**: Search for additional information using DuckDuckGo
- 💬 **Conversational Interface**: Natural language interaction with the AI agent
- 🔄 **Dual Data Sources**: Yahoo Finance + Alpha Vantage fallback for reliability

## Live Demo

🚀 **[Try the live application](https://your-app-name.streamlit.app)**

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-market-ai-agent.git
   cd stock-market-ai-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your API keys
   GROQ_API_KEY=your_actual_groq_api_key
   ALPHA_VANTAGE_API_KEY=your_actual_alpha_vantage_api_key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## API Keys Required

- **Groq API Key**: Get free at [Groq Console](https://console.groq.com/)
- **Alpha Vantage API Key**: Get free at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## Example Questions

- "What's the current price of Apple stock?"
- "What was Bitcoin's price yesterday?"
- "Calculate the average price of Tesla over the last week"
- "What's 15% of 250?"
- "Search for latest Tesla news"

## Technologies Used

- **Streamlit**: Web interface framework
- **LangChain**: Agent framework and tool integration
- **Groq**: Fast LLM inference with open-source models
- **yfinance**: Yahoo Finance API for stock data
- **Alpha Vantage**: Alternative data source for reliability
- **DuckDuckGo Search**: Web search functionality
- **Pandas & NumPy**: Data processing and calculations

## Deployment

This application is deployed on Streamlit Cloud. To deploy your own version:

1. Fork this repository
2. Connect to Streamlit Cloud
3. Add your API keys in the secrets section
4. Deploy!

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
