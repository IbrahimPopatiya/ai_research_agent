import requests

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


AI_KEYWORDS = [
    "ai",
    "machine learning",
    "llm",
    "agent",
    "transformer",
    "neural",
]

def get_top_story_ids():

    response = requests.get(HN_TOP_STORIES)

    if response.status_code != 200:
        return []

    return response.json()[:20]


def get_story_details(story_id):

    url = HN_ITEM_URL.format(story_id)

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()



def is_ai_related(title):

    title = title.lower()

    for keyword in AI_KEYWORDS:
        if keyword in title:
            return True

    return False


def collect_hn_ai_posts():

    posts = []

    story_ids = get_top_story_ids()

    for story_id in story_ids:

        story = get_story_details(story_id)

        if not story:
            continue

        title = story.get("title", "")

        if not is_ai_related(title):
            continue

        post = {
            "title": title,
            "url": story.get("url"),
            "score": story.get("score"),
            "source": "HackerNews"
        }

        posts.append(post)

    return posts