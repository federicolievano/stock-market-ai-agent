import os
import yfinance as yf
import pandas as pd
import numpy as np
import time
import requests
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from langchain.tools import Tool
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS
import json


class StockMarketAgent:
    def __init__(self, groq_api_key: str):
        """Initialize the Stock Market AI Agent"""
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.1
        )
        
        # Create tools for the agent
        self.tools = self._create_tools()
        
        # No need for complex agent, we'll use simple logic
        
    def _create_tools(self) -> list:
        """Create tools for the agent"""
        
        def get_stock_price(symbol: str) -> str:
            """Get current stock price for a given symbol with fallback to Alpha Vantage"""
            try:
                time.sleep(2)  # Add delay to avoid rate limiting
                ticker = yf.Ticker(symbol.upper())
                info = ticker.info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                return f"Current price of {symbol.upper()}: ${current_price}"
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    # Try Alpha Vantage as fallback
                    print(f"Yahoo Finance limitado, usando Alpha Vantage para {symbol}")
                    return self._get_stock_price_alpha_vantage(symbol)
                return f"Error fetching price for {symbol}: {str(e)}"
        
        def get_stock_info(symbol: str) -> str:
            """Get detailed stock information for a given symbol"""
            try:
                time.sleep(2)  # Add delay to avoid rate limiting
                ticker = yf.Ticker(symbol.upper())
                info = ticker.info
                
                result = f"Stock Information for {symbol.upper()}:\n"
                result += f"Current Price: ${info.get('currentPrice', 'N/A')}\n"
                result += f"Previous Close: ${info.get('previousClose', 'N/A')}\n"
                result += f"Market Cap: ${info.get('marketCap', 'N/A')}\n"
                result += f"Volume: {info.get('volume', 'N/A')}\n"
                result += f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
                result += f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}\n"
                
                return result
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    # Try Alpha Vantage as fallback
                    print(f"Yahoo Finance limitado, usando Alpha Vantage para información de {symbol}")
                    return self._get_stock_info_alpha_vantage(symbol)
                return f"Error fetching info for {symbol}: {str(e)}"
        
        def get_historical_data(symbol: str, period: str = "1mo") -> str:
            """Get historical stock data for a given symbol and period"""
            try:
                time.sleep(2)  # Add delay to avoid rate limiting
                ticker = yf.Ticker(symbol.upper())
                hist = ticker.history(period=period)
                
                if hist.empty:
                    return f"No historical data available for {symbol.upper()}"
                
                latest_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2] if len(hist) > 1 else latest_price
                change_percent = ((latest_price - previous_price) / previous_price) * 100
                
                result = f"Historical data for {symbol.upper()} ({period}):\n"
                result += f"Latest Close: ${latest_price:.2f}\n"
                result += f"Previous Close: ${previous_price:.2f}\n"
                result += f"Change: {change_percent:.2f}%\n"
                
                return result
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    # Try Alpha Vantage as fallback
                    print(f"Yahoo Finance limitado, usando Alpha Vantage para datos históricos de {symbol}")
                    return self._get_historical_data_alpha_vantage(symbol, period)
                return f"Error fetching historical data for {symbol}: {str(e)}"
        
        def calculate_average_price(symbol: str, days: int = 7) -> str:
            """Calculate average stock price over specified number of days"""
            try:
                time.sleep(2)  # Add delay to avoid rate limiting
                ticker = yf.Ticker(symbol.upper())
                hist = ticker.history(period=f"{days}d")
                
                if hist.empty:
                    return f"No data available for {symbol.upper()}"
                
                avg_price = hist['Close'].mean()
                result = f"Average price of {symbol.upper()} over last {days} days: ${avg_price:.2f}"
                
                return result
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    # Try Alpha Vantage as fallback
                    print(f"Yahoo Finance limitado, usando Alpha Vantage para promedio de {symbol}")
                    return self._calculate_average_price_alpha_vantage(symbol, days)
                return f"Error calculating average for {symbol}: {str(e)}"
        
        def get_crypto_price(symbol: str) -> str:
            """Get current cryptocurrency price"""
            try:
                time.sleep(2)  # Add delay to avoid rate limiting
                # For crypto, we need to add '-USD' suffix
                crypto_symbol = f"{symbol.upper()}-USD"
                ticker = yf.Ticker(crypto_symbol)
                info = ticker.info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                return f"Current price of {symbol.upper()}: ${current_price}"
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    # Try Alpha Vantage as fallback
                    print(f"Yahoo Finance limitado, usando Alpha Vantage para crypto {symbol}")
                    return self._get_crypto_price_alpha_vantage(symbol)
                return f"Error fetching crypto price for {symbol}: {str(e)}"
        
        def web_search(query: str) -> str:
            """Search the web for information using DuckDuckGo"""
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
                    
                if not results:
                    return "No search results found"
                
                result_text = "Search results:\n"
                for i, result in enumerate(results, 1):
                    result_text += f"{i}. {result['title']}\n   {result['body']}\n\n"
                
                return result_text
            except Exception as e:
                return f"Error performing web search: {str(e)}"
        
        def mathematical_calculation(expression: str) -> str:
            """Perform mathematical calculations safely"""
            try:
                # Remove any potentially dangerous functions
                allowed_names = {
                    k: v for k, v in __builtins__.items()
                    if k in ['abs', 'round', 'min', 'max', 'sum']
                }
                allowed_names.update({
                    'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                    'log': np.log, 'exp': np.exp, 'sqrt': np.sqrt,
                    'pi': np.pi, 'e': np.e
                })
                
                # Evaluate the expression safely
                result = eval(expression, {"__builtins__": {}}, allowed_names)
                return f"Result: {result}"
            except Exception as e:
                return f"Error in calculation: {str(e)}"
        
        # Create tool objects
        tools = [
            Tool(
                name="get_stock_price",
                description="Get current stock price for a given symbol (e.g., AAPL, TSLA, MSFT)",
                func=get_stock_price
            ),
            Tool(
                name="get_stock_info",
                description="Get detailed stock information including price, market cap, volume, etc.",
                func=get_stock_info
            ),
            Tool(
                name="get_historical_data",
                description="Get historical stock data for a given symbol and period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
                func=get_historical_data
            ),
            Tool(
                name="calculate_average_price",
                description="Calculate average stock price over specified number of days",
                func=calculate_average_price
            ),
            Tool(
                name="get_crypto_price",
                description="Get current cryptocurrency price (e.g., BTC, ETH, ADA)",
                func=get_crypto_price
            ),
            Tool(
                name="web_search",
                description="Search the web for information using DuckDuckGo",
                func=web_search
            ),
            Tool(
                name="mathematical_calculation",
                description="Perform mathematical calculations (e.g., '2+2', 'sqrt(16)', 'sin(pi/2)')",
                func=mathematical_calculation
            )
        ]
        
        return tools
    
    def _get_stock_price_alpha_vantage(self, symbol: str) -> str:
        """Get stock price using Alpha Vantage as alternative source"""
        try:
            # Load API key from environment
            env_vars = self._load_env_file()
            api_key = env_vars.get("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                return f"Alpha Vantage API key not configured for {symbol}"
            
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                price = quote.get("05. price", "N/A")
                return f"Current price of {symbol.upper()} (Alpha Vantage): ${price}"
            else:
                return f"No data available for {symbol} from Alpha Vantage"
                
        except Exception as e:
            return f"Error fetching price from Alpha Vantage for {symbol}: {str(e)}"
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        env_vars = {}
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
    
    def _get_stock_info_alpha_vantage(self, symbol: str) -> str:
        """Get detailed stock information using Alpha Vantage as alternative source"""
        try:
            env_vars = self._load_env_file()
            api_key = env_vars.get("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                return f"Alpha Vantage API key not configured for {symbol}"
            
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data and "Symbol" in data:
                result = f"Stock Information for {symbol.upper()} (Alpha Vantage):\n"
                result += f"Current Price: ${data.get('PriceToBookRatio', 'N/A')}\n"
                result += f"Market Cap: ${data.get('MarketCapitalization', 'N/A')}\n"
                result += f"Volume: {data.get('Volume', 'N/A')}\n"
                result += f"52 Week High: ${data.get('52WeekHigh', 'N/A')}\n"
                result += f"52 Week Low: ${data.get('52WeekLow', 'N/A')}\n"
                result += f"Sector: {data.get('Sector', 'N/A')}\n"
                result += f"Industry: {data.get('Industry', 'N/A')}\n"
                return result
            else:
                return f"No detailed data available for {symbol} from Alpha Vantage"
                
        except Exception as e:
            return f"Error fetching detailed info from Alpha Vantage for {symbol}: {str(e)}"
    
    def _get_historical_data_alpha_vantage(self, symbol: str, period: str = "1mo") -> str:
        """Get historical stock data using Alpha Vantage as alternative source"""
        try:
            env_vars = self._load_env_file()
            api_key = env_vars.get("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                return f"Alpha Vantage API key not configured for {symbol}"
            
            # Map period to Alpha Vantage function
            function_map = {
                "1d": "TIME_SERIES_INTRADAY",
                "5d": "TIME_SERIES_INTRADAY", 
                "1mo": "TIME_SERIES_MONTHLY",
                "3mo": "TIME_SERIES_MONTHLY",
                "6mo": "TIME_SERIES_MONTHLY",
                "1y": "TIME_SERIES_MONTHLY",
                "2y": "TIME_SERIES_MONTHLY",
                "5y": "TIME_SERIES_MONTHLY",
                "10y": "TIME_SERIES_MONTHLY",
                "ytd": "TIME_SERIES_MONTHLY",
                "max": "TIME_SERIES_MONTHLY"
            }
            
            function = function_map.get(period, "TIME_SERIES_MONTHLY")
            url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # Find the time series data key
            time_series_key = None
            for key in data.keys():
                if "Time Series" in key:
                    time_series_key = key
                    break
            
            if time_series_key and data[time_series_key]:
                time_series = data[time_series_key]
                dates = sorted(time_series.keys(), reverse=True)
                
                if len(dates) >= 2:
                    latest_date = dates[0]
                    previous_date = dates[1]
                    
                    latest_close = float(time_series[latest_date]["4. close"])
                    previous_close = float(time_series[previous_date]["4. close"])
                    change_percent = ((latest_close - previous_close) / previous_close) * 100
                    
                    result = f"Historical data for {symbol.upper()} ({period}) - Alpha Vantage:\n"
                    result += f"Latest Close: ${latest_close:.2f}\n"
                    result += f"Previous Close: ${previous_close:.2f}\n"
                    result += f"Change: {change_percent:.2f}%\n"
                    return result
            
            return f"No historical data available for {symbol} from Alpha Vantage"
                
        except Exception as e:
            return f"Error fetching historical data from Alpha Vantage for {symbol}: {str(e)}"
    
    def _calculate_average_price_alpha_vantage(self, symbol: str, days: int = 7) -> str:
        """Calculate average stock price using Alpha Vantage as alternative source"""
        try:
            env_vars = self._load_env_file()
            api_key = env_vars.get("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                return f"Alpha Vantage API key not configured for {symbol}"
            
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "Time Series (Daily)" in data and data["Time Series (Daily)"]:
                time_series = data["Time Series (Daily)"]
                dates = sorted(time_series.keys(), reverse=True)
                
                # Get the last N days
                recent_dates = dates[:min(days, len(dates))]
                prices = []
                
                for date in recent_dates:
                    close_price = float(time_series[date]["4. close"])
                    prices.append(close_price)
                
                if prices:
                    avg_price = sum(prices) / len(prices)
                    result = f"Average price of {symbol.upper()} over last {len(prices)} days (Alpha Vantage): ${avg_price:.2f}"
                    return result
            
            return f"No data available for calculating average of {symbol} from Alpha Vantage"
                
        except Exception as e:
            return f"Error calculating average from Alpha Vantage for {symbol}: {str(e)}"
    
    def _get_crypto_price_alpha_vantage(self, symbol: str) -> str:
        """Get cryptocurrency price using Alpha Vantage as alternative source"""
        try:
            env_vars = self._load_env_file()
            api_key = env_vars.get("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                return f"Alpha Vantage API key not configured for {symbol}"
            
            # Alpha Vantage uses different symbols for crypto
            crypto_symbols = {
                'BTC': 'BTC',
                'ETH': 'ETH',
                'ADA': 'ADA',
                'DOGE': 'DOGE'
            }
            
            crypto_symbol = crypto_symbols.get(symbol.upper(), symbol.upper())
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={crypto_symbol}&to_currency=USD&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "Realtime Currency Exchange Rate" in data:
                exchange_rate = data["Realtime Currency Exchange Rate"]
                price = exchange_rate.get("5. Exchange Rate", "N/A")
                return f"Current price of {symbol.upper()} (Alpha Vantage): ${price}"
            else:
                return f"No crypto data available for {symbol} from Alpha Vantage"
                
        except Exception as e:
            return f"Error fetching crypto price from Alpha Vantage for {symbol}: {str(e)}"
    
    def _decide_tool(self, message: str) -> str:
        """Robust logic to decide which tool to use"""
        message_lower = message.lower()
        
        # Mathematical calculations (highest priority)
        math_patterns = [
            r'\d+\s*[+\-*/]\s*\d+',  # Basic operations
            r'\d+\s*%\s*of\s*\d+',   # Percentage calculations
            r'sqrt\s*\(',            # Square root
            r'sin\s*\(|cos\s*\(|tan\s*\('  # Trigonometric functions
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, message_lower):
                return 'mathematical_calculation'
        
        # Check for math operators
        if any(char in message for char in ['+', '-', '*', '/', '%', '=', 'sqrt', 'sin', 'cos', 'tan', 'log']):
            return 'mathematical_calculation'
        
        # Stock price queries (very common)
        price_patterns = [
            r'precio|price|cotización|cuesta|cost|valor|value',
            r'cuánto cuesta|how much|what.*price',
            r'precio actual|current price'
        ]
        
        for pattern in price_patterns:
            if re.search(pattern, message_lower):
                # Check if it's crypto or stock
                if any(crypto in message_lower for crypto in ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'criptomoneda']):
                    return 'get_crypto_price'
                else:
                    return 'get_stock_price'
        
        # Detailed stock information
        info_patterns = [
            r'información|info|detalles|details|market cap|volumen|volume',
            r'capitalización|capitalization|52.*week|high|low'
        ]
        
        for pattern in info_patterns:
            if re.search(pattern, message_lower):
                return 'get_stock_info'
        
        # Historical data
        historical_patterns = [
            r'histórico|historical|ayer|yesterday|cambio|change|trend',
            r'último|last|semana|week|mes|month|año|year'
        ]
        
        for pattern in historical_patterns:
            if re.search(pattern, message_lower):
                return 'get_historical_data'
        
        # Average calculations
        average_patterns = [
            r'promedio|average|media|mean',
            r'última semana|last week|últimos días|last days'
        ]
        
        for pattern in average_patterns:
            if re.search(pattern, message_lower):
                return 'calculate_average_price'
        
        # Web search
        search_patterns = [
            r'buscar|search|noticias|news|encontrar|find',
            r'últimas noticias|latest news|información sobre'
        ]
        
        for pattern in search_patterns:
            if re.search(pattern, message_lower):
                return 'web_search'
        
        # If we detect a stock symbol but no specific tool, default to stock price
        symbol = self._extract_symbol_robust(message)
        if symbol:
            return 'get_stock_price'
        
        return None
    
    def _extract_symbol_robust(self, message: str) -> str:
        """Robustly extract stock/crypto symbol from message"""
        message_upper = message.upper()
        
        # Common stock symbols mapping
        stock_mapping = {
            'APPLE': 'AAPL', 'AAPL': 'AAPL',
            'TESLA': 'TSLA', 'TSLA': 'TSLA', 
            'MICROSOFT': 'MSFT', 'MSFT': 'MSFT',
            'GOOGLE': 'GOOGL', 'GOOGL': 'GOOGL',
            'AMAZON': 'AMZN', 'AMZN': 'AMZN',
            'META': 'META', 'FACEBOOK': 'META',
            'NETFLIX': 'NFLX', 'NFLX': 'NFLX',
            'NVIDIA': 'NVDA', 'NVDA': 'NVDA',
            'BITCOIN': 'BTC', 'BTC': 'BTC',
            'ETHEREUM': 'ETH', 'ETH': 'ETH'
        }
        
        # Check for direct symbol matches first
        for key, symbol in stock_mapping.items():
            if key in message_upper:
                return symbol
        
        # Look for 3-5 letter uppercase symbols (typical stock symbols)
        symbol_pattern = r'\b[A-Z]{3,5}\b'
        symbols = re.findall(symbol_pattern, message_upper)
        
        # Filter out common words that aren't stock symbols
        exclude_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'MAN', 'MEN', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}
        
        for symbol in symbols:
            if symbol not in exclude_words and len(symbol) >= 3:
                return symbol
        
        return None
    
    def _extract_symbol(self, message: str, tool_type: str) -> str:
        """Extract symbol from message"""
        message_lower = message.lower()
        
        if tool_type in ['get_stock_price', 'get_stock_info', 'get_historical_data', 'calculate_average_price']:
            if 'apple' in message_lower or 'aapl' in message_lower:
                return 'AAPL'
            elif 'tesla' in message_lower or 'tsla' in message_lower:
                return 'TSLA'
            elif 'microsoft' in message_lower or 'msft' in message_lower:
                return 'MSFT'
            elif 'google' in message_lower or 'googl' in message_lower:
                return 'GOOGL'
            elif 'amazon' in message_lower or 'amzn' in message_lower:
                return 'AMZN'
        
        elif tool_type == 'get_crypto_price':
            if 'bitcoin' in message_lower or 'btc' in message_lower:
                return 'BTC'
            elif 'ethereum' in message_lower or 'eth' in message_lower:
                return 'ETH'
        
        return None
    
    def chat(self, message: str) -> str:
        """Process a user message and return agent response"""
        try:
            # Decide which tool to use
            tool_name = self._decide_tool(message)
            
            if tool_name:
                # Find the tool function
                tool_func = None
                for tool in self.tools:
                    if tool.name == tool_name:
                        tool_func = tool.func
                        break
                
                if tool_func:
                    print(f"🔧 Using tool: {tool_name}")  # Debug info
                    
                    # Extract parameters based on tool type
                    if tool_name in ['get_stock_price', 'get_stock_info', 'get_crypto_price']:
                        symbol = self._extract_symbol_robust(message)
                        print(f"📊 Detected symbol: {symbol}")  # Debug info
                        if symbol:
                            result = tool_func(symbol)
                        else:
                            result = "Por favor especifica el símbolo de la acción o criptomoneda (ej: Apple, Tesla, Bitcoin, AAPL, TSLA)"
                    
                    elif tool_name in ['get_historical_data', 'calculate_average_price']:
                        symbol = self._extract_symbol_robust(message)
                        print(f"📊 Detected symbol: {symbol}")  # Debug info
                        if symbol:
                            if tool_name == 'get_historical_data':
                                result = tool_func(symbol, "1mo")
                            else:
                                result = tool_func(symbol, 7)
                        else:
                            result = "Por favor especifica el símbolo de la acción (ej: Apple, Tesla, AAPL, TSLA)"
                    
                    elif tool_name == 'web_search':
                        result = tool_func(message)
                    
                    elif tool_name == 'mathematical_calculation':
                        # Extract mathematical expression more robustly
                        math_patterns = [
                            r'\d+\s*[+\-*/]\s*\d+',  # Basic operations
                            r'\d+\s*%\s*of\s*\d+',   # Percentage
                            r'sqrt\s*\([^)]+\)',     # Square root
                            r'sin\s*\([^)]+\)|cos\s*\([^)]+\)|tan\s*\([^)]+\)',  # Trig functions
                            r'[\d\+\-\*\/\(\)\.\s]+'  # General math expression
                        ]
                        
                        expression = None
                        for pattern in math_patterns:
                            matches = re.findall(pattern, message)
                            if matches:
                                expression = max(matches, key=len).strip()
                                break
                        
                        if expression:
                            print(f"🧮 Detected expression: {expression}")  # Debug info
                            result = tool_func(expression)
                        else:
                            result = "Por favor proporciona una expresión matemática válida (ej: 2+2, 15% of 250)"
                    
                    return result
            
            # If no specific tool matches, use LLM for general questions
            response = self.llm.invoke(message)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            return f"Error processing your request: {str(e)}"


# Example usage
if __name__ == "__main__":
    # You would need to set your GROQ API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("Please set your GROQ_API_KEY environment variable")
    else:
        agent = StockMarketAgent(api_key)
        
        # Test the agent
        test_questions = [
            "What is the current price of Apple stock?",
            "What was Bitcoin's price yesterday?",
            "Calculate the average price of Tesla over the last week",
            "What's 15% of 250?"
        ]
        
        for question in test_questions:
            print(f"\nQ: {question}")
            print(f"A: {agent.chat(question)}")
