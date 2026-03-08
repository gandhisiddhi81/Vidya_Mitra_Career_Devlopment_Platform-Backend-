import os
import requests
from typing import List, Dict, Any

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def get_recommended_certifications(role: str) -> List[Dict[str, Any]]:
    if not NEWS_API_KEY:
        print("⚠️ NEWS_API_KEY not found in environment variables")
        return get_fallback_certifications(role)

    try:
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params={
                'q': f'{role} certification OR {role} professional course',
                'sortBy': 'relevancy',
                'pageSize': 5,
                'apiKey': NEWS_API_KEY,
                'language': 'en'
            }
        )
        response.raise_for_status()
        data = response.json()

        articles = data.get('articles', [])
        if articles:
            return [{
                'name': article['title'],
                'provider': article['source']['name'],
                'description': article['description'],
                'link': article['url']
            } for article in articles]

        return get_fallback_certifications(role)
    except Exception as e:
        print(f"News API Error (Certifications): {e}")
        return get_fallback_certifications(role)

def get_fallback_certifications(role: str) -> List[Dict[str, Any]]:
    lower_role = role.lower()
    
    if 'software' in lower_role or 'developer' in lower_role:
        return [
            { "name": "AWS Certified Developer - Associate", "provider": "Amazon Web Services", "link": "https://aws.amazon.com/certification/certified-developer-associate/" },
            { "name": "Google Professional Cloud Developer", "provider": "Google Cloud", "link": "https://cloud.google.com/certification/cloud-developer" },
            { "name": "Microsoft Certified: Azure Developer Associate", "provider": "Microsoft", "link": "https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/" }
        ]
    
    if 'data' in lower_role or 'analyst' in lower_role:
        return [
            { "name": "Google Data Analytics Professional Certificate", "provider": "Coursera / Google", "link": "https://www.coursera.org/professional-certificates/google-data-analytics" },
            { "name": "IBM Data Science Professional Certificate", "provider": "Coursera / IBM", "link": "https://www.coursera.org/professional-certificates/ibm-data-science" },
            { "name": "Tableau Desktop Specialist", "provider": "Tableau", "link": "https://www.tableau.com/learn/certification/desktop-specialist" }
        ]

    return [
        { "name": "PMP (Project Management Professional)", "provider": "PMI", "link": "https://www.pmi.org/certifications/project-management-pmp" },
        { "name": "Google Project Management Professional Certificate", "provider": "Coursera / Google", "link": "https://www.coursera.org/professional-certificates/google-project-management" }
    ]
