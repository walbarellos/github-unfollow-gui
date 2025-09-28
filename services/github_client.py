import os
import time
from typing import Dict, List, Set, Tuple

import requests

TOKEN = os.getenv("GITHUB_TOKEN", "")
USERNAME = os.getenv("USERNAME", "")
TIMEOUT = int(os.getenv("REQUESTS_TIMEOUT", "15"))
SLEEP_S = float(os.getenv("REQUESTS_SLEEP_SECONDS", "0.8"))

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

API = "https://api.github.com"

def _paged(url: str) -> List[dict]:
    page = 1
    acc: List[dict] = []
    while True:
        resp = requests.get(f"{url}&per_page=100&page={page}", headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code != 200:
            raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text[:300]}")
        data = resp.json()
        if not data:
            break
        acc.extend(data)
        page += 1
    return acc

def list_followers(username: str) -> Set[str]:
    data = _paged(f"{API}/users/{username}/followers?since=0")
    return {u["login"] for u in data}

def list_following(username: str) -> Set[str]:
    data = _paged(f"{API}/users/{username}/following?since=0")
    return {u["login"] for u in data}

def fetch_user_public(login: str) -> dict:
    resp = requests.get(f"{API}/users/{login}", headers=HEADERS, timeout=TIMEOUT)
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text[:300]}")
    return resp.json()

def enrich_users(logins: List[str]) -> List[dict]:
    """Enriquece com metadados úteis para filtros/ordenação."""
    enriched = []
    for i, login in enumerate(logins, 1):
        u = fetch_user_public(login)
        enriched.append({
            "login": u.get("login"),
            "html_url": u.get("html_url"),
            "avatar_url": u.get("avatar_url"),
            "name": u.get("name"),
            "bio": u.get("bio"),
            "company": u.get("company"),
            "blog": u.get("blog"),
            "location": u.get("location"),
            "email": u.get("email"),
            "hireable": u.get("hireable"),
            "type": u.get("type"),  # User/Organization
            "site_admin": u.get("site_admin"),
            "public_repos": u.get("public_repos"),
            "followers": u.get("followers"),
            "following": u.get("following"),
            "created_at": u.get("created_at"),
            "updated_at": u.get("updated_at"),
        })
        time.sleep(SLEEP_S)  # respeitar rate-limit
    return enriched

def delete_follow(login: str) -> Tuple[bool, int]:
    resp = requests.delete(f"{API}/user/following/{login}", headers=HEADERS, timeout=TIMEOUT)
    ok = resp.status_code == 204
    return ok, resp.status_code
