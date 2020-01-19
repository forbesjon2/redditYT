from RedditUtils import RedditUtils
from subprocess import call
import datetime
import random

def daysSinceEpoch():
    epoch = datetime.datetime.utcfromtimestamp(0)
    today = datetime.datetime.today()
    d = today - epoch
    return str(d.days)



def runMain(utilsInstance, subReddit):
    submissionsList = utilsInstance.returnTop()
    postNos = input("enter post numbers (separated by a space): ")
    numTopComments = int(input("how many top comments: "))
    globalCount = 0

    for post in postNos.split(" "):
        globalCount += 1
        title = submissionsList[int(post)].title
        postHtml = utilsInstance.generatePostTitle(submissionsList[int(post)])
        utilsInstance.genVideoClip(postHtml, submissionsList[int(post)].title, globalCount)

        topComments = utilsInstance.getTopComments(numTopComments, submissionsList[int(post)].comments.list())        

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
        fileName = subReddit + "_" + daysSinceEpoch() + "_" + str(random.randint(1,1000000))
        # combine the individual video files into one file and put it in /output
        call(["./cleanCombine.sh " + fileName], shell=True)
        # create a thumbnail
        utilsInstance.createThumbnail(title, fileName)
        youtubeUpload(title, submissionsList[int(post)].url, subReddit, fileName)

def youtubeUpload(videoTitle, videoDesc, board, fileName):
    #upload video to youtube
    videoParams = '--title "' + videoTitle +  '" --client-secrets="./yt_creds_file.json" --category=Entertainment --description="' + videoDesc + '" --tags="reddit,' + board + ',trending" --default-language="en" --privacy="private" --default-audio-language="en" --embeddable=True --thumbnail ./output/' + fileName + '.jpg ./output/' + fileName + '_vid.mp4'
    print("calling...")
    print("youtube-upload " + videoParams)
    call(["youtube-upload " + videoParams], shell=True)