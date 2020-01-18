from RedditUtils import RedditUtils

topNews = RedditUtils(10, "news", "day", True)

submissionsList = topNews.returnTop()
postNos = input("enter post numbers (separated by a space): ")
numTopComments = int(input("how many top comments: "))

for post in postNos.split(" "):
    topComments = topNews.getTopComments(numTopComments, submissionsList[int(post)])
    print(topComments)

# post.comments.list()
# topComments = sr.getTopComments(10, post)
# for comment in topComments:
