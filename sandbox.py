import praw
from ScrapeReddit import ScrapeReddit

reddit = praw.Reddit(client_id='T_2TohvDxVxynw', client_secret="yQzjuCPfBijseEYLnrezj05ELKQ",
                     password='moKkun-dotrif-sezxo0', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
                     username='markermal3')
                
sr = ScrapeReddit(reddit, 10, "news", "day", True)
submissionsList = sr.returnTop()

post = submissionsList[0].comments.list()
topComments = sr.getTopComments(10, post)
for comment in topComments:
    print(comment[0].body)
    print(comment[1].body)
    print ("\n")
