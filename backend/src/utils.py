"""Utility functions for AWS Bedrock integration."""

import json
import os
from pathlib import Path
from typing import Generator

import boto3
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

KB_ID = "JGMPKF6VEI"
FALLBACK_PHRASE = "sorry, i am unable to assist you with this request"


def _get_aws_credentials():
    """Get AWS credentials from environment."""
    return {
        "region_name": "us-east-1",
        "aws_access_key_id": os.getenv("ACCESS_KEY"),
        "aws_secret_access_key": os.getenv("SECRET_KEY"),
    }


def create_agent():
    """Create Bedrock agent runtime client."""
    return boto3.client("bedrock-agent-runtime", **_get_aws_credentials())


def create_bedrock_runtime():
    """Create Bedrock runtime client."""
    return boto3.client("bedrock-runtime", **_get_aws_credentials())


def _format_claude_request(user_query: str) -> dict:
    """Format request body for Claude models."""
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": user_query}]
    }


def retrieve_and_generate_stream(user_query: str, model_name: str) -> Generator[str, None, None]:
    """Stream responses from knowledge base."""
    bedrock_agent = create_agent()

    stream_resp = bedrock_agent.retrieve_and_generate_stream(
        input={"text": user_query},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KB_ID,
                "modelArn": model_name,
            },
        },
    )

    for event in stream_resp["stream"]:
        if "output" in event:
            yield event["output"]["text"]


def generate_general_stream(user_query: str, model_name: str) -> Generator[str, None, None]:
    """Stream general LLM response with real-time streaming."""
    bedrock_runtime = create_bedrock_runtime()
    body = _format_claude_request(user_query)
    
    try:
        response = bedrock_runtime.invoke_model_with_response_stream(
            body=json.dumps(body),
            modelId=model_name,
            accept="application/json",
            contentType="application/json",
        )
        
        # Process Claude streaming response
        for event in response.get('body'):
            chunk = json.loads(event['chunk']['bytes'].decode())
            
            if 'delta' in chunk and 'text' in chunk['delta']:
                yield chunk['delta']['text']
            elif 'content_block_delta' in chunk:
                delta = chunk['content_block_delta'].get('delta', {})
                if 'text' in delta:
                    yield delta['text']
                    
    except Exception as e:
        yield f"Error generating response: {str(e)}"


def smart_generate_stream(user_query: str, model_name: str) -> Generator[str, None, None]:
    """Try KB first, fallback to general LLM if no answer."""
    try:
        # Try KB first and collect initial chunks to check if we get a good response
        kb_chunks = []
        kb_generator = retrieve_and_generate_stream(user_query, model_name)
        
        # Collect first few chunks to determine if KB has useful content
        for i, chunk in enumerate(kb_generator):
            kb_chunks.append(chunk)
            if i >= 2:  # Check first 3 chunks
                break
        
        # Check if we should continue with KB or fallback
        kb_preview = "".join(kb_chunks)
        if kb_preview.strip() and FALLBACK_PHRASE not in kb_preview.lower():
            # KB has good content, yield what we have and continue
            for chunk in kb_chunks:
                yield chunk
            
            # Continue with remaining KB chunks
            for chunk in kb_generator:
                yield chunk
        else:
            # KB didn't have good content, use general LLM
            yield from generate_general_stream(user_query, model_name)
                
    except Exception as e:
        # Error fallback - yield error message then try general LLM
        yield f"Knowledge base error: {str(e)}. Switching to general AI...\n\n"
        yield from generate_general_stream(user_query, model_name)
