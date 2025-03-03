import os
import json
import groq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        api_key = os.environ.get('GROQ_API_KEY')
        print("Loaded API Key:", api_key)  # Debugging line

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Check your environment variables or .env file.")

        self.client = groq.Client(api_key=api_key)
        self.model = "llama3-8b-8192"  # Choose an appropriate model
        self.system_prompt = """You are a helpful assistant similar to Meta AI. 
        You provide clear, concise, and accurate information. 
        When you don't know something, you admit it instead of making up information."""

    
    def get_response(self, message_history):
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            for msg in message_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
                top_p=1,
            )
            
            return {
                "status": "success",
                "message": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }