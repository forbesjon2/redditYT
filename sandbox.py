from RedditUtils import RedditUtils

topNews = RedditUtils(10, "news", "day", True)

submissionsList = topNews.returnTop()
postNos = input("enter post numbers (separated by a space): ")
numTopComments = int(input("how many top comments: "))
globalCount = 0

for post in postNos.split(" "):
    topComments = topNews.getTopComments(numTopComments, submissionsList[int(post)].comments.list())
    # # Post title then html to img
    # topNews.htmlToImg(topNews.generatePostTitle(submissionsList[int(post)]), globalCount)
    
    # # one comment
    # topNews.htmlToImg(topNews.generateOneComment(submissionsList[int(post)].comments.list()[0]), globalCount)

    # two comments
    topNews.htmlToImg(topNews.generateTwoComments(submissionsList[int(post)].comments.list()[0], submissionsList[int(post)].comments.list()[1]), globalCount)


# post.comments.list()
# topComments = sr.getTopComments(10, post)
# for comment in topComments:
