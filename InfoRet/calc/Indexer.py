from nltk.corpus import stopwords
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
        with open('C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\data.json', 'r') as fp:
            self.data = json.load(fp)

        for key, value in self.data.items():
            for eachTitle in value:
                self.AddToWordList(eachTitle)

    def AddToWordList(self, title):
        if title[0] in self._allTitles:
            return
        self.docIdToTitle[self._docID] = title
        self._docID += 1
        for eachWord in title[0].split(' '):
            if eachWord not in self.stopWords:
                self._allWords.add(eachWord)

    def IndexAllWords(self):
        docIDs = []
        for eachWord in self._allWords:
            for key, val in self.docIdToTitle.items():
                if (eachWord.lower() in val[0].lower()):
                    docIDs.append(key)
            self.wordToDocList[eachWord] = docIDs
            docIDs = []

    def SaveIndexedState(self):
        with open('indexed.json', 'w') as fp:
            json.dump(self.wordToDocList, fp, sort_keys=True, indent=4)

    def LoadIndexedState(self):
        with open('C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\indexed.json', 'r') as fp:
            self.wordToDocList = json.load(fp)

    def GetHtmlBody(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Giggle</title>
</head>
<body>"""

    def GetHtmlEndBody(self):
        return """</body>
</html>"""

    def Search(self, searchTerms):
        relevantDocs = []

        if searchTerms in self.data:
            return self.data[searchTerms]

        for eachWord in searchTerms.split(' '):
            if (searchTerms not in self.stopWords) and (eachWord not in self.stopWords):
                if eachWord in self.wordToDocList:
                    relevantDocs.append(self.wordToDocList[eachWord])

        intersection = set.intersection(*[set(eachSet) for eachSet in relevantDocs])
        print (intersection)
        
        finalText = self.GetHtmlBody()
        finalText += """<center>"""
        resultantDocs = []
        for docID in intersection:
            resultantDocs.append(self.docIdToTitle[docID])
            finalText += self.docIdToTitle[docID][0] + """<br>"""
        finalText += """</center>"""
        finalText += self.GetHtmlEndBody()

        with open("C:\\Users\\Saravanacoumar\\courseWorkInfoRet\\InfoRet\\templates\\result2.html", 'w', encoding='utf8') as f:
            f.writelines(finalText)
            f.flush()
        return resultantDocs