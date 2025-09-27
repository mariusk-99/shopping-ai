#!/usr/bin/env python3
"""
Simple test to verify Google Gemini API connection
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_gemini_connection():
    """Test basic Gemini API connection"""
    
    api_key = os.getenv('GOOGLE_GEMINI_API_KEY') or os.getenv('GOOGLE_VEO2_API_KEY')
    if not api_key:
        print("❌ No API key found in environment variables")
        return
    
    # Test with a simple text prompt
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello, can you respond with a simple greeting?"
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 100
        }
    }
    
    print("🔗 Testing Gemini API connection...")
    print(f"🔑 API key (first 20 chars): {api_key[:20]}...")
    
    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    text = parts[0].get("text", "")
                    print("✅ Connection successful!")
                    print(f"🤖 Gemini response: {text}")
                    return True
            print("⚠️ Unexpected response format")
            print(f"Response: {result}")
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Error response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"🚨 Connection error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    test_gemini_connection()