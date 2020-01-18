


class ScrapeReddit:
    def __init__(self, redditInstance, numberOfTopPosts=10, board="news", timeFrame="day", verbose=True):
        self.board = board
        self.verbose = verbose
        self.timeFrame = timeFrame
        self.redditInstance = redditInstance
        self.numberOfTopPosts = numberOfTopPosts

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