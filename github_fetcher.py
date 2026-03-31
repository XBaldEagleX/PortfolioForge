"""
GitHub Fetcher for PortfolioForge
Pulls your repos, user info, and stats using the official GitHub API.
"""

from github import Github, Auth
from config import GITHUB_TOKEN, GITHUB_USERNAME
import json
from datetime import datetime

def fetch_github_data() -> dict:
    """
    Fetch all GitHub data needed for the portfolio.
    Returns a clean dictionary with user info and list of repos.
    """
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        raise ValueError("Missing GITHUB_TOKEN or GITHUB_USERNAME in .env")

    # Connect to GitHub (new recommended way - no deprecation warning)
    g = Github(auth=Auth.Token(GITHUB_TOKEN))
    
    # Get your user
    user = g.get_user(GITHUB_USERNAME)
    
    # Fetch all your repos
    repos = user.get_repos()
    
    # Build list of repos
    repo_list = []
    for repo in repos:
        repo_list.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description or "",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language or "None",
            "topics": repo.topics,
            "html_url": repo.html_url,
            "updated_at": repo.updated_at.strftime("%Y-%m-%d") if repo.updated_at else None,
            "is_fork": repo.fork,
        })
    
    # Sort by most recently updated (outside the loop!)
    repo_list.sort(key=lambda x: x["updated_at"] or "1900-01-01", reverse=True)
    
    # Build final data structure
    data = {
        "user": {
            "name": user.name or user.login,
            "login": user.login,
            "bio": user.bio or "",
            "location": user.location or "",
            "avatar_url": user.avatar_url,
            "html_url": user.html_url,
            "public_repos": user.public_repos,
            "followers": user.followers,
            "following": user.following,
        },
        "repositories": repo_list,
        "total_repos_fetched": len(repo_list),
        "fetched_at": datetime.now().isoformat(),
    }
    
    print(f"Successfully fetched {len(repo_list)} repositories for {user.login}")
    return data


# Quick test when running this file directly
if __name__ == "__main__":
    # Make sure output folder exists
    import os
    os.makedirs("output", exist_ok=True)
    
    data = fetch_github_data()
    # Save a sample JSON so you can see what it looks like
    with open("output/github_data_sample.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Sample data saved to output/github_data_sample.json")
