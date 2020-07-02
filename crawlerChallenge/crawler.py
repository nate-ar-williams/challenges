#!/usr/bin/python3

from urllib.request import urlopen
from html.parser import HTMLParser
import re, sys

url = 'https://en.wikipedia.org/wiki/Microsoft'
target = 'History'

# header type wikipedia uses for sections
headerType = 'h2'

class WordCountParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isRightSection = False
        self.sectionText = ''

    def handle_starttag(self, tag, attributes):
        for key, value in attributes:
            if key == 'id' and value == target:
                self.isRightSection = True
        if self.isRightSection and tag == headerType:
            self.isRightSection = False

    def handle_data(self, data):
        if self.isRightSection:
            self.sectionText += data;

def printCommonWords(wordsDict, n=10):
    sortedWords = sorted(wordsDict, key=wordsDict.__getitem__, reverse = True)
    for i in range(n):
        print(sortedWords[i] + ': ' + str(wordsDict[sortedWords[i]]))

if __name__ == '__main__':
    # default number of words to show
    n = 10
    wordsToExclude = []

    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            wordsToExclude.append(sys.argv[i])
 
    html = ''
    with urlopen(url) as response:
        html = response.read()

    parser = WordCountParser()
    # html is bytes ,convert to utf-8 string
    parser.feed(html.decode())

    sectionWords = parser.sectionText.split()
    pattern = re.compile('[\W_0-9]+')
    words = {}
    for word in sectionWords:
        strippedWord = pattern.sub('', word).lower()
        if strippedWord in words:
            words[strippedWord] += 1
        else:
            words[strippedWord] = 1

    del words['']
    for word in wordsToExclude:
        if word in words:
            del words[word]

    printCommonWords(words, n)
