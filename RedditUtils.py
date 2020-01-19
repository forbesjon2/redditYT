import os
import sys
import boto3
import praw
import json
import imgkit
from subprocess import call


class RedditUtils:
    def __init__(self, numberOfTopPosts=10, board="news", timeFrame="day", verbose=True):
        # load credentials
        credentials = {}
        with open("credentials.json", "r") as creds:
            credentials = json.load(creds)
            creds.close()

        self.redditInstance = praw.Reddit(client_id=credentials["reddit_client_id"], client_secret=credentials["reddit_client_secret"],
                     password=credentials["reddit_password"], user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15', username=credentials["reddit_username"])
        self.board = board
        self.verbose = verbose
        self.timeFrame = timeFrame
        self.numberOfTopPosts = numberOfTopPosts
        self.polly_client = boto3.Session(aws_access_key_id=credentials["aws_access_key_id"], aws_secret_access_key=credentials["aws_secret_access_key"], region_name='us-west-2').client('polly')


    def returnTop(self):
        """
        prints and Returns a list of the top submissions
        
        returns a list of submissions objects see the following for info:
        https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
        """
        count = 0
        submissions = []
        for submission in self.redditInstance.subreddit(self.board).top(self.timeFrame):
            if count > self.numberOfTopPosts:
                break
            print(str(count) + ". " +  submission.title + "\n")
            submissions.append(submission)
            count += 1
        return submissions



    def getTopComments(self, numTopComments, post):
        """
        this will return the top comments and the reply attached
        to each of the top comments

        given submissionsList from returnTop()...
        post = submissionsList[0].comments.list()

        for comments and replies you will need to use....
        comment.author, comment.body, comment.score
        (https://praw.readthedocs.io/en/latest/code_overview/models/comment.html)

        format
        [[comment, reply], [comment, reply]]
        """
        res = []
        count = 0
        while count < numTopComments:
            res.append([post[count], post[count].replies.list()[0]])
            count += 1
        return res


    def getRawText(self, message, forAmazonTTS):
        """
        removes the links and formats it to amazonTTS if need be
        """
        # remove links
        message = str(re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', message))
        if forAmazonTTS:
            message = message.replace("*","").replace("\"", "&quot;").replace("&", "&amp;").replace("'", "&apos;").replace("<", "&lt;").replace(">","&gt;")
        return message


    def generateOneComment(self, comment):
        """
        returns the HTML for one comment
        """
        author = comment.author.name
        points = comment.score
        post = comment.body
        cwd = os.getcwd() + "/starterHTML/"
        content = ""
        with open("./starterHTML/OneComment.txt", "r") as outfile:
            content = outfile.read()
            outfile.close()
        content = content.replace("^^author^^", author).replace("^^points^^", str(points))
        content = content.replace("^^content^^", post).replace("^^CWD^^", cwd)
        return content


    def generateTwoComments(self, comment, comment2):
        """
        returns the HTML for two comments
        """
        author = comment.author.name
        points = comment.score
        post = comment.body
        author2 = comment2.author.name
        points2 = comment2.score
        post2 = comment2.body
        cwd = os.getcwd() + "/starterHTML/"
        content = ""
        with open("./starterHTML/TwoComment.txt", "r") as outfile:
            content = outfile.read()
            outfile.close()
        content = content.replace("^^author^^", author).replace("^^points^^", str(points)).replace("^^content^^", post)
        content = content.replace("^^author2^^", author2).replace("^^points2^^", str(points2)).replace("^^content2^^", post2).replace("^^CWD^^", cwd)
        return content


    def generatePostTitle(self, post):
        """
        Returns the HTML for the post title
        """
        board = post.subreddit.display_name
        author = post.author.name
        title = post.title
        score = post.score
        postText = post.selftext
        print(title)
        print(postText)
        content = ""
        with open("./starterHTML/PostTitle.txt", "r") as outfile:
            content = outfile.read()
            outfile.close()
            content = content.replace("^^board^^", board).replace("^^author^^", author).replace("^^upvotes^^",str(score))
            content = content.replace("^^title^^", title).replace("^^content^^", postText)
        return content


    def number_padding(self, number):
        """
        adds zero padding for numbers up to 100. This is so that the files using the numbering
        scheme are ordered correctly when sorted and concatenated with ffmpeg
        1 -> 001
        10 --> 010
        100 --> 100
        """
        if number >= 100:
            return str(number)
        return  "00" + str(number) if (number < 10 and number < 100) else "0" + str(number)

    def textToMp3(self, message, globalCount):
        # text to mp3. save to ./audio
        audioLocation = "audio/out" + str(self.number_padding(globalCount)) + ".mp3"
        audioTextSSML = '<speak><prosody rate="1.05">' + self.genRawText(message, True) + '<break time="0.25s" /> </prosody></speak>'
        response = self.polly_client.synthesize_speech(VoiceId='Matthew',OutputFormat='mp3', Text=audioTextSSML, TextType= 'ssml')
        file = open(audioLocation, 'wb')
        file.write(response['AudioStream'].read())
        file.close()

    def htmlToImg(self, html, globalCount):
        imageLocation = "img/out" + str(self.number_padding(globalCount)) + ".jpg"
        imgkit.from_string(html, imageLocation, options={"xvfb":""})