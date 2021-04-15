from requests import get as fetch
from bs4 import BeautifulSoup
import json

ROOT_URL = 'https://scholar.google.co.uk'

class Crawler:

    def __init__(self, link, depth):
        self._link = link
        self._depth = depth
        self.authorsToPublications = {}

    def GetLink(self):
        return self._link

    def CrawlBooks(self, link):
        htmlTextRet = fetch(link).text
        parsedHtmlText = BeautifulSoup(htmlTextRet, "lxml")
        publicationList = parsedHtmlText.findAll('td', class_='gsc_a_t')
        citationsList = parsedHtmlText.findAll('td', class_='gsc_a_c')
        yearOfPublicationsList = parsedHtmlText.findAll('td', class_='gsc_a_y')
        publications = []
        for (eachBook, citation, year) in zip(publicationList, citationsList, yearOfPublicationsList):
            publications.append(tuple((eachBook.a.text, citation.a.text, year.span.text, link)))
        return publications

    def CleanUpTheLink(self, link):
        link = link.replace('\\x3d', '=')
        link = link.replace('\\x26', '&')
        link = link.replace('\'', '')
        link = link.replace('&oe=ASCII', '')
        link = link.replace('window.location=', ROOT_URL)
        return link

    def StartCrawling(self):
        queue = []
        queue.append(self._link)
        
        while (queue and self._depth):
            firstOnQueue = queue.pop()
            try:
                htmlTextRet = fetch(firstOnQueue).text
                parsedHtmlText = BeautifulSoup(htmlTextRet, "lxml")

                for eachLink in parsedHtmlText.findAll('h3', class_='gs_ai_name'):
                    try:
                        profileLink = eachLink.a.get('href')
                        publications = self.CrawlBooks(ROOT_URL + profileLink)
                        if publications:
                            self.authorsToPublications[eachLink.a.text] = publications
                    except:
                        pass
                self._depth -= 1

                for eachButton in parsedHtmlText.findAll('button'):
                    if (eachButton.get('aria-label') == 'Next'):
                        link = self.CleanUpTheLink(eachButton.get('onclick'))
                        queue.append(link)
                        break
            except:
                pass
        for key, value in self.authorsToPublications.items():
            print (key)
            print (value)
            print()

        with open('data.json', 'w') as fp:
            json.dump(self.authorsToPublications, fp, sort_keys=True, indent=4)