from RedditUtils import RedditUtils


def runMain(utilsInstance):
    submissionsList = utilsInstance.returnTop()
    postNos = input("enter post numbers (separated by a space): ")
    numTopComments = int(input("how many top comments: "))
    globalCount = 0

    for post in postNos.split(" "):
        globalCount += 1
        topComments = utilsInstance.getTopComments(numTopComments, submissionsList[int(post)].comments.list())
        # Post title then html to img
        utilsInstance.htmlToImg(utilsInstance.generatePostTitle(submissionsList[int(post)]), globalCount)
        

        # commentsList = submissionsList[int(post)].comments.list()
        for comment, reply in topComments:
            # first comment, create image & audioFile
            globalCount += 1
            html = utilsInstance.generateOneComment(comment)
            utilsInstance.genVideoClip(html, comment.body, globalCount)
            
            # create image and audiofile for second comment
            globalCount += 1
            html = utilsInstance.generateTwoComments(comment, reply)
            utilsInstance.genVideoClip(html, reply.body, globalCount)



