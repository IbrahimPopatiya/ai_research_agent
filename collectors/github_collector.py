import requests
from database.crud import save_ai_tool


GITHUB_API_URL = "https://api.github.com/search/repositories"

MIN_STARS = 50

AI_KEYWORDS = [
    "ai",
    "machine learning",
    "llm",
    "agent",
    "rag",
    "transformer"
]


def search_github_repositories(keyword):
    params = {
        "q": keyword,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    try:
        response = requests.get(GITHUB_API_URL, params=params)

        if response.status_code != 200:
            print("GitHub API error")
            return []

        data = response.json()

        return data.get("items", [])
    except Exception as e:
        print("Github request failed: ",e)
        return []    


def extract_repo_data(repo):
    stars = repo["stargazers_count"]

    if stars < MIN_STARS:
        return None

    return {
        "name": repo["name"],
        "description": repo["description"],
        "stars": stars,
        "language": repo["language"],
        "url": repo["html_url"]
    }    


def collect_ai_tools():
    collected_tools = []

    for keyword in AI_KEYWORDS:
        repositories = search_github_repositories(keyword)

        for repo in repositories:
            tool = extract_repo_data(repo)
            if tool is not None:
                collected_tools.append(tool)

    return collected_tools

def collect_and_store_ai_tools():

    tools = collect_ai_tools()
    print("Total tools discovered:", len(tools))


    for tool in tools:
        save_ai_tool(tool)
    print("GitHub collection finished")
    print("AI tools saved to database")