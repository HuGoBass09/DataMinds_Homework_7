"""FastAPI backend server for the bedrock chat bot."""

import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict

sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from utils import smart_generate_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BAKU_TZ = timezone(timedelta(hours=4))

app = FastAPI(
    title="Azercell Knowledge Base Model Backend",
    description="REST API for Azercell Knowledge Base Model",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Data(BaseModel):
    prompt: str
    modelName: str


@app.get("/health")
def health() -> Dict[str, Any]:
    utc_time = datetime.now(timezone.utc).isoformat()
    baku_time = datetime.now(BAKU_TZ).isoformat()
    return {"status": "healthy", "utc_time": utc_time, "baku_time": baku_time}


@app.post("/generate")
async def generate(data: Data):
    prompt = data.prompt
    model_name = data.modelName

    return StreamingResponse(
        smart_generate_stream(
            user_query=prompt,
            model_name=model_name,
        ),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering if present
        }
    )
