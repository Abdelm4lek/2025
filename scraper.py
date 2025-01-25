import praw, json
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from prawcore.exceptions import RequestException, ResponseException, OAuthException, PrawcoreException

#* Login credentials
config = ConfigParser()
config.read('./config.ini')

try:
    reddit = praw.Reddit(
        user_agent=config['X']["user_agent"],
        client_id=config['X']["client_id"],
        client_secret=config['X']["client_secret"],
        refresh_token=config['X']["refresh_token"]
    )
    # Test authentication
    reddit.user.me() 
    print("Authenticated successfully.")
except (OAuthException, PrawcoreException) as e:
    print(f"Authentication failed: {e}")
    exit(1)


def fetch_reddit_posts_batch(subreddits, search_keywords, min_comments=50, max_posts=10):
    """
    Fetch Reddit posts using batch processing for multiple subreddits and keywords.
    """
    for subreddit in subreddits:
        subreddit_instance = reddit.subreddit(subreddit)
        for keyword in search_keywords:
            try:
                yield from (
                    {
                        "id": post.id,
                        "title": post.title,
                        "url": post.url,
                        "num_comments": post.num_comments,
                        "upvotes": post.score,
                        "created_utc": post.created_utc
                    }
                    for post in subreddit_instance.search(keyword, sort="new", limit=max_posts)
                    if post.num_comments >= min_comments
                )
            except (RequestException, ResponseException) as e:
                print(f"Error fetching posts from subreddit '{subreddit}' with keyword '{keyword}': {e}")

def fetch_comments_concurrently(posts, max_threads=5):
    """
    Fetch comments from posts concurrently using ThreadPoolExecutor.
    """
    all_comments = []

    def process_post(post):
        try:
            submission = reddit.submission(id=post['id'])
            submission.comments.replace_more(limit=None)  # Expand "load more comments"
            return [
                {
                    "post_id": post['id'],
                    "post_title": post['title'],
                    "comment_id": comment.id,
                    "comment_body": comment.body,
                    "comment_score": comment.score,
                }
                for comment in submission.comments.list()
            ]
        except (RequestException, ResponseException) as e:
            print(f"Error fetching comments for post '{post['title']}': {e}")
            return []  # Return an empty list if fetching fails

    with ThreadPoolExecutor(max_threads) as executor:
        try:
            results = executor.map(process_post, posts)
            for comments in results:
                all_comments.extend(comments)
        except Exception as e:
            print(f"Error during concurrent comment fetching: {e}")

    return all_comments

def save_to_json(data, filename="reddit_comments.json"):
    """
    Save data to a JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")


# Parameters
subreddits = ["soccer", "football"]
search_keywords = ["match", "player", "goal"]
min_comments = 50
max_posts = 10
max_threads = 5  

# Step 1: Fetch posts in batches
try:
    posts = list(fetch_reddit_posts_batch(subreddits, search_keywords, min_comments, max_posts))
    print(f"Fetched {len(posts)} posts.")
except Exception as e:
    print(f"Error during post fetching: {e}")
    posts = []

# Step 2: Fetch comments concurrently
if posts:
    try:
        comments = fetch_comments_concurrently(posts, max_threads)
        print(f"Fetched {len(comments)} comments.")

        # Step 3: Save comments to JSON
        save_to_json(comments, "reddit_comments.json")
    except Exception as e:
        print(f"Error during comment fetching or saving: {e}")
else:
    print("No posts found with the given criteria.")
