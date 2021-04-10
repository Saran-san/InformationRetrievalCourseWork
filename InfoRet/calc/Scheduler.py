from threading import Thread
from time import sleep
from . import Indexer

EVERY_WEEK = 604800 #seconds

class Scheduler(Thread):
    def __init__(self, indexer):
        Thread.__init__(self)
        self.indexer = indexer
    
    def run(self):
        while (True):
            self.indexer = Indexer.Indexer()
            self.indexer.IndexAllWords()
            self.indexer.SaveIndexedState()
            sleep(EVERY_WEEK)