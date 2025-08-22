# Backend - Azercell Knowledge Base Chatbot

FastAPI backend server that handles AWS Bedrock integration and knowledge base queries.

![Build Status](https://github.com/Emillock/my-ml-proj/actions/workflows/ci-build.yaml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://shields.io/)

## Features

- **AWS Bedrock Integration**: Direct connection to AWS Bedrock knowledge base
- **Streaming Responses**: Real-time response streaming for better UX
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **CORS Support**: Configured for frontend integration
- **Health Monitoring**: Health check endpoints with timezone support

## Project Structure

```
backend/
├── app.py                     # FastAPI application entry point
├── main.py                    # Alternative entry point
├── src/
│   ├── utils.py              # AWS Bedrock utilities
│   ├── features/
│   │   └── build_features.py # Feature engineering
│   ├── models/
│   │   ├── train_model.py    # Model training utilities
│   │   └── predict_model.py  # Model prediction utilities
│   └── visualization/
│       └── visualize.py      # Data visualization
├── reports/                   # Generated analysis and reports
├── notebooks/                 # Jupyter notebooks for exploration
└── models/                    # Trained model artifacts
```

## API Endpoints

### Health Check
```
GET /health
```
Returns server health status with UTC and Baku timezone information.

### Generate Response
```
POST /generate
```
Streams responses from AWS Bedrock knowledge base.

**Request Body:**
```json
{
  "prompt": "Your question here",
  "modelName": "anthropic.claude-3-haiku-20240307-v1:0"
}
```

## Environment Setup

Create a `.env` file in the backend directory:

```env
ACCESS_KEY="your_aws_access_key"
SECRET_KEY="your_aws_secret_key"
```

## Development

### Using uv (Recommended)

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

```bash
# Lint code
uvx ruff check .

# Format code
uvx black .

# Sort imports
uvx isort .

# Auto-fix issues
uvx ruff check --fix .
```

## Docker

The backend is containerized and runs on port 8000:

```bash
docker build -t backend -f Dockerfile .
docker run -p 8000:8000 backend
```

## AWS Configuration

The application connects to AWS Bedrock with the following configuration:
- **Region**: us-east-1
- **Knowledge Base ID**: JGMPKF6VEI
- **Supported Models**: Claude 3 Haiku, Claude 3.5 Sonnet

Ensure your AWS credentials have appropriate permissions for:
- `bedrock-agent-runtime:RetrieveAndGenerateStream`
- Access to the specified knowledge base

## Structure
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── uv.lock   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `uv lock > uv.lock`
    │
    ├── pyptoject.toml    <- makes project uv installable (uv installs) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py


--------


## Getting started (uv)
```bash
# create venv and sync (will create uv.lock)
uv sync

# add a runtime dependency
uv add numpy

# run code
uv run python -m src.models.train_model
```

## Code quality (ruff, isort, black via uvx)
### Run tools in ephemeral envs — no dev dependencies added to your project.

#### Lint (no changes)
```bash
# Lint entire repo
uvx ruff check .
```

#### Auto-fix
```bash
# 1) Sort imports
uvx isort .

# 2) Format code
uvx black .

# 3) Apply Ruff’s safe fixes (entire repo)
uvx ruff check --fix .
```
> Also remove unused imports/variables:
> ```bash
> uvx ruff check --fix --unsafe-fixes .
> ```
