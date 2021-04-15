from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import json

class Indexer(object):
    """Index all the workds in each doc/title"""
    def __init__(self):
        self._allWords = set()
        self._allTitles = set()
        self._docID = 0
        self.docIdToTitle = {}
        self.wordToDocList = {}
        self.stopWords = stopwords.words('english')
        self.data = dict()
        self.ps = PorterStemmer()
        with open('C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\data.json', 'r') as fp:
            self.data = json.load(fp)

        for key, value in self.data.items():
            for eachTitle in value:
                self.AddToWordList(eachTitle)
        print ("Indexer Initialised")

    def AddToWordList(self, title):
        if title[0] in self._allTitles:
            return
        self.docIdToTitle[self._docID] = title
        self._docID += 1
        for eachWord in word_tokenize(title[0]):
            if eachWord not in self.stopWords:
                self._allWords.add(self.ps.stem(eachWord))

    def IndexAllWords(self):
        docIDs = []
        for eachWord in self._allWords:
            for key, val in self.docIdToTitle.items():
                if (eachWord.lower() in val[0].lower()):
                    docIDs.append(key)
            self.wordToDocList[eachWord] = docIDs
            docIDs = []
        print ("Indexing finished")

    def SaveIndexedState(self):
        with open('C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\indexed.json', 'w') as fp:
            json.dump(self.wordToDocList, fp, sort_keys=True, indent=4)

    def LoadIndexedState(self):
        with open('C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\indexed.json', 'r') as fp:
            self.wordToDocList = json.load(fp)
            print ("Indexed File Loaded")

    def GetHtmlBody(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Giggle</title>
</head>
<body>
<center>"""

    def GetHtmlEndBody(self):
        return """</center>
        </body>
</html>"""

    def WrapWithLink(self, title, link):
        return """<a href=""" + link + """>""" + title + """</a>"""

    def Search(self, searchTerms):
        relevantDocs = []

        if searchTerms in self.data:
            finalText = self.GetHtmlBody()
            for eachTitle in self.data[searchTerms]:
                #finalText += eachTitle[0] + """<br>"""
                relevantDocs.append(eachTitle)
            relevantDocs.sort(key=lambda x: int(x[1]), reverse=True)
            for eachTitle in relevantDocs:
                finalText += self.WrapWithLink(eachTitle[0], eachTitle[3]) + """<br>"""
                finalText += "cited on " + str(eachTitle[1]) + ", " + str(eachTitle[2]) + """<br>"""
                finalText += """<br>"""
            finalText += self.GetHtmlEndBody()
            with open("C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\templates\\result2.html", 'w', encoding='utf8') as f:
                f.writelines(finalText)
                f.flush()
            return

        for eachWord in word_tokenize(searchTerms):
            if (searchTerms not in self.stopWords) and (eachWord not in self.stopWords):
                if self.ps.stem(eachWord) in self.wordToDocList:
                    relevantDocs.append(self.wordToDocList[self.ps.stem(eachWord)])

        intersection = set.intersection(*[set(eachSet) for eachSet in relevantDocs])
        print (intersection)
        
        finalText = self.GetHtmlBody()

        resultantDocs = []
        for docID in intersection:
            resultantDocs.append(self.docIdToTitle[docID])

        resultantDocs.sort(key=lambda x: int(x[1]), reverse=True)

        print (resultantDocs)
        for docID in resultantDocs:
            finalText += self.WrapWithLink(docID[0], docID[3]) +  """<br>"""
            finalText += "cited on " + str(docID[1]) + ", " + str(docID[2]) + """<br>"""
            finalText += """<br>"""
        finalText += self.GetHtmlEndBody()

        with open("C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\templates\\result2.html", 'w', encoding='utf8') as f:
            f.writelines(finalText)
            f.flush()
        return resultantDocs