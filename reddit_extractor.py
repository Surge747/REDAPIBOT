# reddit_extractor.py

import praw

def fetch_reddit_posts(subreddit_name, sort='hot', limit=10):
    reddit = praw.Reddit(
        client_id='',
        client_secret='',
        user_agent=''
    )

    subreddit = reddit.subreddit(subreddit_name)

    # Fetch posts based on the sort method
    if sort == 'new':
        posts = subreddit.new(limit=limit)
    elif sort == 'top':
        posts = subreddit.top(limit=limit)
    elif sort == 'controversial':
        posts = subreddit.controversial(limit=limit)
    elif sort == 'rising':
        posts = subreddit.rising(limit=limit)
    else:
        posts = subreddit.hot(limit=limit)

    post_list = []
    for post in posts:
        if not post.stickied and len(post.selftext) > 10:
            post_data = {
                'title': post.title,
                'selftext': post.selftext,
                'url': post.url,
                'id': post.id,
                'author': str(post.author),
            }
            post_list.append(post_data)

    return post_list

def fetch_reddit_post_by_url(post_url, comments_limit=0):
    try:
        reddit = praw.Reddit(
            client_id='',
            client_secret='',
            user_agent=''
        )

        submission = reddit.submission(url=post_url)
        submission.comments.replace_more(limit=0)
        comments = submission.comments[:comments_limit] if comments_limit > 0 else []

        post_data = {
            'title': submission.title,
            'selftext': submission.selftext,
            'url': submission.url,
            'id': submission.id,
            'author': str(submission.author),
            'subreddit': str(submission.subreddit),
            'comments': []
        }

        for comment in comments:
            post_data['comments'].append({
                'author': str(comment.author),
                'body': comment.body
            })
        return post_data

    except Exception as e:
        print(f"An error occurred while fetching the post: {e}")
        return None

