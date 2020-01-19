from RedditUtils import RedditUtils
from Run import runMain
import os
import sys

topNews = RedditUtils(10, "news", "day", True)

runMain(topNews, "news")