# Frontend - Azercell Knowledge Base Chatbot

This is the Streamlit frontend application for the Azercell Knowledge Base chatbot system.

## Features

- Interactive chat interface for querying Azercell's knowledge base
- Support for multiple AI models (Claude 3 Haiku, Claude 3.5 Sonnet)
- Chat history management with create/delete functionality
- Real-time streaming responses from the backend
- Responsive UI with customizable sidebar

## Project Structure

```
frontend/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration settings
├── apps/
│   └── mcp_playground.py     # Main chat interface
├── services/
│   ├── chat_service.py       # Chat session management
│   └── ai_service.py         # AI service integration
├── ui_components/
│   ├── main_components.py    # Main UI components
│   └── sidebar_components.py # Sidebar UI components
├── utils/
│   ├── ai_prompts.py         # AI prompt templates
│   ├── async_helpers.py      # Async utility functions
│   └── tool_schema_parser.py # Tool schema parsing
└── .streamlit/
    ├── config.toml           # Streamlit configuration
    └── style.css             # Custom CSS styles
```

## Installation & Setup

The frontend is containerized using Docker. See the main project README for setup instructions.

## Configuration

Model selection and other settings are configured in `config.py`:

```python
MODEL_OPTIONS = {
    "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "Claude 3.5 Sonnet": "anthropic.claude-3-5-sonnet-20240620-v1:0",
}
```

## Development

For local development, install dependencies and run:

```bash
uv sync
uv run streamlit run app.py
```

The application will be available at `http://localhost:8501`.
