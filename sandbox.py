import praw
reddit = praw.Reddit(client_id='T_2TohvDxVxynw', client_secret="yQzjuCPfBijseEYLnrezj05ELKQ",
                     password='moKkun-dotrif-sezxo0', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
                     username='markermal3')

for submission in reddit.subreddit('news').hot(limit=25):
    print(submission.title)