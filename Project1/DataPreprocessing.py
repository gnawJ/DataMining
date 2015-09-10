__author__ = 'Po Yao'
__author__ = 'Jun wang'

import re
import os, sys
import nltk
from nltk.stem.lancaster import LancasterStemmer
from BeautifulSoup import BeautifulSoup

# functions go here
def checkOnlyContainNumAndComma(string):
    flag = True
    validSet = ['1','2','3','4','5','6','7','8','9','0',',','.']
    for c in string:
        if c not in validSet:
            return False
    return flag

# def isfloat(value):
#   try:
#     float(value)
#     return True
#   except ValueError:
#     return False

def buildingIntermediateData1(soup,intermediateData1):
    # iterate every article in the file
    articles = soup.findAll('reuters')
    for article in articles:

        # find date and use it as key
        dates = article.findAll('date')
        # it should contain only one date else throw exception
        if len(dates) != 1:
            raise ValueError('more than one date')
        dateEntry = str(dates[0].next.string)

        # find topics
        topicsList=[] # a list contains all the topics
        topics = article.findAll('topics')
        # it should contain only one topic else throw exception
        if len(topics) != 1:
            raise ValueError('more than one topic')
        Ds = topics[0].findAll('d')
        if len(Ds) != 0:
           for D in Ds:
               topicsList.append(str(D.next.string))

        # find places
        placesList=[] # a list contains all the places
        places = article.findAll('places')
        # it should contain only one place else throw exception
        if len(places) != 1:
            raise ValueError('more than one place')
        Ds = places[0].findAll('d')
        if len(Ds) != 0:
           for D in Ds:
               placesList.append(str(D.next.string))

        # process body
        bodys = article.findAll('body')
        if len(bodys) != 1:
            raise ValueError('more than one body')
        bodyDict = buidBodyDict(bodys[0])
        intermediateData1[dateEntry] = [topicsList,placesList,bodyDict]
    return
def buidBodyDict(body):
    gabageWords = ['.',',','<','!','@','#','$','%','^','&','*','(',')','_','+','=','?','/','~','`',';',':','>','reut']
    bodyDictionary = {} # {key: word, value: occur times}
    bodyString = str(body.next.string)
    tokens = nltk.word_tokenize(bodyString,language='english')
    st = LancasterStemmer()
    # iterate every word in tokens. For efficient we want to do everything in this loop such as stemming and counting...
    for word in tokens:
        # check whether it is gabbage
        if (word not in gabageWords) and (not checkOnlyContainNumAndComma(str(word))):
            # make sure it is not a number
            # stemming
            word = str(st.stem(word))
            # adding to dictionary
            if word not in bodyDictionary:
                bodyDictionary[word] = 1
            else:
                oldCount = bodyDictionary[word]
                bodyDictionary[word] = oldCount + 1
    return bodyDictionary

# declare some data structure we need
# a dictionary structure, whose key is date of each article and value
# is a list structure {['topics'],['places'], [all the words in each article]}
intermediateData1 = {}

# read all files in a directory
# TO Do ask user to type the path of data directory
path = '/Users/junwang/Desktop/DataMining/Project1/TestDataset/'
dir = os.listdir(path)
# iterate each article in each file
for file in dir:
    sgm = open(path + file).read()
    soup = BeautifulSoup(''.join(sgm))
    # processing raw data step 1: build intermediateData1
    buildingIntermediateData1(soup,intermediateData1)
print intermediateData1



