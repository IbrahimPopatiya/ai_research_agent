import requests



AI_SUBREDDITS = [
    "MachineLearning",
    "artificial",
    "LocalLLaMA",
    "AItools"
]

AI_KEYWORDS = [
    "ai",
    "machine learning",
    "llm",
    "agent",
    "transformer",
    "neural",
]


def is_ai_related(title):

    title = title.lower()

    for keyword in AI_KEYWORDS:
        if keyword in title:
            return True

    return False



HEADERS = {
    "User-Agent": "ai-research-agent"
}


def fetch_subreddit_posts(subreddit):

    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=20"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Reddit request failed")
        return []

    data = response.json()

    return data["data"]["children"]



def extract_post_data(post):

    post_data = post["data"]

    return {
        "title": post_data["title"],
        "url": "https://reddit.com" + post_data["permalink"],
        "score": post_data["score"],
        "source": "Reddit"
    }

def collect_reddit_ai_posts():

    posts = []

    for subreddit in AI_SUBREDDITS:

        raw_posts = fetch_subreddit_posts(subreddit)

        for post in raw_posts:

            title = post["data"]["title"]

            if not is_ai_related(title):
                continue

            extracted = extract_post_data(post)

            posts.append(extracted)

    return posts