from RedditUtils import RedditUtils
from Run import runMain
import os
topNews = RedditUtils(10, "news", "day", True)

runMain(topNews, "news")
