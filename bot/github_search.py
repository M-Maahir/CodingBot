import os
import requests  # <-- This is the missing import
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def search_github_repos(query, max_results=3):
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results,
    }

    url = "https://api.github.com/search/repositories"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        items = response.json().get("items", [])
        return [
            {
                "name": repo["full_name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "description": repo["description"] or "No description."
            }
            for repo in items
        ]
    else:
        return []

# Optional: if you're also using this
def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("name", username),
            "login": data["login"],
            "url": data["html_url"],
            "avatar": data["avatar_url"],
            "bio": data.get("bio", "No bio available."),
            "repos": data["public_repos"],
            "followers": data["followers"],
            "following": data["following"]
        }
    else:
        return None
