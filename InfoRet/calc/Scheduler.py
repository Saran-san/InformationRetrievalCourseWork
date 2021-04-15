from threading import Thread
from time import sleep
from . import Indexer
from . import Crawler

EVERY_WEEK = 604800 #seconds

class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.crawler = Crawler.Crawler("https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779", 20)
        self.indexer = None   
    
    def GetIndexer(self):
        return self.indexer

    def run(self):
        while (True):
            self.crawler.StartCrawling()
            self.indexer = Indexer.Indexer()
            self.indexer.IndexAllWords()
            self.indexer.SaveIndexedState()
            self.indexer.LoadIndexedState()
            sleep(EVERY_WEEK)