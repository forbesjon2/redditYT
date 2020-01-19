from RedditUtils import RedditUtils
from Run import runMain

topNews = RedditUtils(10, "news", "day", True)

runMain(topNews)