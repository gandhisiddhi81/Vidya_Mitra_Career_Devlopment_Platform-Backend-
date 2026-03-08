import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json

load_dotenv()

async def test_gemini():
    print("\n🔍 Testing Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY missing")
        return False
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = await model.generate_content_async("Hello, are you working?")
        print(f"✅ Gemini Response: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return False

async def test_grok():
    print("\n🔍 Testing Grok API...")
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        print("❌ GROK_API_KEY missing")
        return False
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-2",
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.3
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Grok Response: {response.json()['choices'][0]['message']['content'][:50]}...")
            return True
        else:
            print(f"❌ Grok Status Code: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Grok Error: {e}")
        return False

async def test_youtube():
    print("\n🔍 Testing YouTube API...")
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("❌ YOUTUBE_API_KEY missing")
        return False
    try:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={
                'part': 'snippet',
                'q': 'Python FastAPI',
                'maxResults': 1,
                'type': 'video',
                'key': api_key
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ YouTube API working, found {len(response.json().get('items', []))} videos")
            return True
        else:
            print(f"❌ YouTube Status Code: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ YouTube Error: {e}")
        return False

async def test_news():
    print("\n🔍 Testing News API...")
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("❌ NEWS_API_KEY missing")
        return False
    try:
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params={
                'q': 'technology',
                'pageSize': 1,
                'apiKey': api_key
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ News API working, found {response.json().get('totalResults')} results")
            return True
        else:
            print(f"❌ News Status Code: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ News Error: {e}")
        return False

async def main():
    print("🚀 Starting API Diagnostics...")
    results = await asyncio.gather(
        test_gemini(),
        test_grok(),
        test_youtube(),
        test_news()
    )
    print("\n" + "="*30)
    print(f"Final Report: {sum(results)}/4 APIs working")
    print("="*30)

if __name__ == "__main__":
    asyncio.run(main())
