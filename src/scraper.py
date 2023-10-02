import praw
import json
import os
import time
import logging
from prawcore.exceptions import TooManyRequests, RequestException, PrawcoreException

# Set up logging
logging.basicConfig(filename='logs/reddit_scraper.log', level=logging.INFO)

# Define the file paths
SUBEREDDITS_FILE = "files/subreddits.txt"
MINED_SUBREDDITS_FILE = "files/mined_subreddits.txt"

# Define Reddit API credentials
CLIENT_ID = "WbZPw1kfqgln7VbQbtWAHA"
CLIENT_SECRET = "zGYuO1y5hN9Zott_VgEnNdSpVDphdg"
USERNAME = "toninlolo"
PASSWORD = "safadona123"

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent="python:datacraper:v1.0.0 (by u/AntonioFerreiraMine>)"
)

# Save the subreddit data to a JSON file
def save_data_on_file(subreddit_name, subreddit_data):
    output_file = os.path.join("output/"f"{subreddit_name.lower()}_data.json")

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(subreddit_data, json_file, indent=4)

    with open(MINED_SUBREDDITS_FILE, "a") as file:
        file.write(subreddit_name.lower() + "\n")

# Process a subreddit and save its data to a JSON file.
def process_subreddit(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name.lower())
        top_posts = subreddit.top(limit=None)
        subreddit_data = []

        # Create a dictionary for each post with desired data
        for i, post in enumerate(top_posts, start=1):
            post_data = {
                "Author": post.author.name if post.author else "Deleted",
                "Title": post.title,
                "Score": post.score,
                "Content": post.selftext,
                "Tags": ', '.join(post.link_flair_richtext[0].get('t')) if post.link_flair_richtext and isinstance(post.link_flair_richtext[0].get('t'), (list, tuple)) else '',
                "Date": post.created_utc,
                "Comments": []
            }

            if i in [200, 400, 600, 800]:
                print("Waiting for 120 seconds")
                time.sleep(120)

            # Process each comment and its replies
            for comment in post.comments:
                if isinstance(comment, praw.models.Comment):
                    comment_data = {
                        "Author": comment.author.name if comment.author else "Deleted",
                        "Body": comment.body,
                        "Replies": []
                    }

                    # Process replies to the current comment
                    for reply in comment.replies:
                        if isinstance(reply, praw.models.Comment):
                            reply_data = {
                                "Author": reply.author.name if reply.author else "Deleted",
                                "Body": reply.body
                            }
                            comment_data["Replies"].append(reply_data)

                    post_data["Comments"].append(comment_data)

            # Append the post data to the subreddit data list
            subreddit_data.append(post_data)

            print(f"Post {i} from subreddit '{subreddit_name.lower()}' added: {post.title}")

        # Save the subreddit data to a JSON file
        save_data_on_file(subreddit_name, subreddit_data)
        
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
        exit()

    except TooManyRequests:
        logging.error(f"sub: {subreddit_name.lower()}, post: {i}. Rate limit reached.")
        logging.info("Waiting for 300 seconds.")
        time.sleep(300)

    except (RequestException, PrawcoreException) as e:
        logging.error(f"An error occurred in subreddit '{subreddit_name.lower()}': {e}")
        logging.info("Skipping subreddit due to error.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.info("Skipping subreddit due to error.")

def main():
    mined_subreddits = set()

    # Read all subreddits from a file and process each one
    with open(MINED_SUBREDDITS_FILE, "r") as file:
        mined_subreddits = set(file.read().splitlines())

    with open(SUBEREDDITS_FILE, "r") as file:
        subreddit_names = file.read().splitlines()

    for subreddit_name in subreddit_names:
        if subreddit_name.lower() in mined_subreddits:
            logging.info(f"Skipping subreddit '{subreddit_name.lower()}' as it has already been mined.")
            continue

        process_subreddit(subreddit_name)
        mined_subreddits.add(subreddit_name.lower())

    logging.info("Done.\n")
    print("Done.")

if __name__ == "__main__":
    main()
    exit()
