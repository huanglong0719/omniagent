import os
import requests
import time
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="omniagent/.env")

class LLMClient:
    """
    LLMClient: A wrapper around the Google Gemini API.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = os.getenv("GEMINI_API_URL")
        self.http_proxy = os.getenv("HTTP_PROXY")
        self.https_proxy = os.getenv("HTTPS_PROXY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
    async def generate(self, messages: list, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Generates a response from the Gemini API with retry logic for 503/429 errors.
        """
        user_prompt = messages[-1]["content"] if messages else "Hello"
        
        payload = {
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        proxies = {}
        if self.http_proxy: proxies["http"] = self.http_proxy
        if self.https_proxy: proxies["https"] = self.https_proxy

        max_retries = 3
        retry_delay = 2 # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                # Using requests.post (synchronous) for simplicity in this prototype
                response = requests.post(
                    self.api_url, 
                    headers=headers, 
                    params=params, 
                    json=payload,
                    proxies=proxies,
                    timeout=60
                )
                
                if response.status_code == 503 or response.status_code == 429:
                    print(f"[LLM Retry] Server error {response.status_code}. Attempt {attempt+1}/{max_retries}. Retrying in {retry_delay}s...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                    continue
                
                response.raise_for_status()
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[LLM Error] Final attempt failed: {e}")
                    return f"Error generating response after {max_retries} attempts: {str(e)}"
                print(f"[LLM Error] Attempt {attempt+1} failed: {e}. Retrying...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
