# Urban Analysis Agent

This project is a Streamlit-based web application that implements an AI-powered agent for analyzing climate conditions, particularly focused on paragliding activities. The agent uses LangGraph and Ollama to provide intelligent responses about weather, wind conditions, and paragliding suitability for any city.

## Features

- Interactive chat interface with agent streaming
- Integration with Open Meteo APIs for real-time data
- Session-based conversation memory
- Tools for weather, wind, and paragliding condition analysis

## Requirements

- Python 3.8+
- Ollama running locally with a model that can access tools (qwen3:8b recommended)
- Internet connection for weather API access

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PedroBazzarella/paragliding-analyst-agent
   cd urban-analysis-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure Ollama:
   - Ensure Ollama is installed and running
   - Update `agent/config.py` with your Ollama base URL and model name if necessary
   ```python
   OLLAMA_BASE_URL = "http://localhost:11434" # default ollama url
   OLLAMA_MODEL = "qwen3:8b" # recommended model
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `main.py`: Simple script for testing
- `agent/`: Core agent logic and configuration
- `tools/`: Utility functions for weather and paragliding data
- `utils/`: Helper functions for coordinates and weather retrieval
