import os
import requests
from typing import List, Dict, Any

async def search_videos(keywords: str, max_results: int = 5) -> List[Dict[str, Any]]:
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        print("⚠️ YOUTUBE_API_KEY not found in environment variables")
        return []

    try:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={
                'part': 'snippet',
                'q': keywords,
                'maxResults': max_results,
                'type': 'video',
                'key': key,
                'relevanceLanguage': 'en'
            }
        )
        response.raise_for_status()
        data = response.json()

        return [{
            'id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['medium']['url'],
            'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        } for item in data.get('items', [])]
    except Exception as e:
        print(f"YouTube API Error: {e}")
        return []

async def search_playlists(keywords: str, max_results: int = 3) -> List[Dict[str, Any]]:
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        return []

    try:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={
                'part': 'snippet',
                'q': keywords,
                'maxResults': max_results,
                'type': 'playlist',
                'key': key
            }
        )
        response.raise_for_status()
        data = response.json()

        return [{
            'id': item['id']['playlistId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['medium']['url'],
            'link': f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
        } for item in data.get('items', [])]
    except Exception as e:
        print(f"YouTube API Error (Playlists): {e}")
        return []
