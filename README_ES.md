# Stock Market AI Agent

Una aplicación de IA conversacional que proporciona información bursátil en tiempo real, precios de criptomonedas y realiza operaciones matemáticas.

## Características

- 📈 **Precios de Acciones en Tiempo Real**: Obtén precios actuales de cualquier símbolo bursátil
- 💰 **Datos de Criptomonedas**: Bitcoin, Ethereum y otros precios de crypto
- 📊 **Análisis Histórico**: Ve datos históricos y calcula cambios porcentuales
- 🧮 **Operaciones Matemáticas**: Realiza cálculos y operaciones de porcentaje
- 🔍 **Búsqueda Web**: Busca información adicional usando DuckDuckGo
- 💬 **Interfaz Conversacional**: Interacción en lenguaje natural con el agente de IA
- 🔄 **Doble Fuente de Datos**: Yahoo Finance + Alpha Vantage como respaldo para confiabilidad

## Demo en Vivo

🚀 **[Prueba la aplicación en vivo](https://your-app-name.streamlit.app)**

## Inicio Rápido

### Desarrollo Local

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/yourusername/stock-market-ai-agent.git
   cd stock-market-ai-agent
   ```

2. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura variables de entorno**
   ```bash
   # Crea archivo .env con tus API keys
   GROQ_API_KEY=tu_groq_api_key_real
   ALPHA_VANTAGE_API_KEY=tu_alpha_vantage_api_key_real
   ```

4. **Ejecuta la aplicación**
   ```bash
   streamlit run app.py
   ```

## API Keys Requeridas

- **Groq API Key**: Obtén gratis en [Groq Console](https://console.groq.com/)
- **Alpha Vantage API Key**: Obtén gratis en [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## Preguntas de Ejemplo

- "¿Cuál es el precio actual de Apple?"
- "¿Cuál fue el precio de Bitcoin ayer?"
- "Calcula el promedio de Tesla de la última semana"
- "¿Cuánto es 15% de 250?"
- "Busca las últimas noticias de Tesla"

## Tecnologías Utilizadas

- **Streamlit**: Framework de interfaz web
- **LangChain**: Framework de agentes e integración de herramientas
- **Groq**: Inferencia rápida de LLM con modelos de código abierto
- **yfinance**: API de Yahoo Finance para datos bursátiles
- **Alpha Vantage**: Fuente de datos alternativa para confiabilidad
- **DuckDuckGo Search**: Funcionalidad de búsqueda web
- **Pandas & NumPy**: Procesamiento de datos y cálculos

## Despliegue

Esta aplicación está desplegada en Streamlit Cloud. Para desplegar tu propia versión:

1. Haz fork de este repositorio
2. Conecta a Streamlit Cloud
3. Agrega tus API keys en la sección de secretos
4. ¡Despliega!

## Licencia

Licencia MIT - ver archivo LICENSE para detalles.

## Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de enviar un Pull Request.
