# project 1 for Data mining course
# Date: 9/13/2015
__author__ = 'Po Yao'
__author__ = 'Jun wang'

import math
import os, sys
import nltk
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('Cp1252')

# functions go here

# def round_sig(x, sig=2):
#     return round(x, sig-int(floor(log10(x)))-1)

# eliminate some numbers in raw data such as 1,000
def checkOnlyContainNumAndComma(string):
    flag = True
    validSet = ['0','2','3','4','5','6','7','8','9','1',',','.']
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

# build an important intermediate datum, which will be used in the whole project
# formation of intermediateData1 is introduced below
def buildingIntermediateData1(soup,intermediateData1,totalNumber):
    # iterate every article in the file
    totalNumber = 0
    articles = soup.findAll('reuters')
    for article in articles:
        totalNumber += 1
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
        if len(bodys) == 1:
            bodyDict = buidBodyDict(str(bodys[0].next.string))
            intermediateData1[dateEntry] = [topicsList,placesList,bodyDict]
        else:
            mutiBodyString=''
            for body in bodys:
                mutiBodyString += str(body.next.string)
                bodyDict = buidBodyDict(mutiBodyString)
                intermediateData1[dateEntry] = [topicsList,placesList,bodyDict]
    return totalNumber

# preprocessing the body of each article
def buidBodyDict(bodyString):
    gabageWords = ['.',',','<','!','@','#','$','%','^','&','*','(',')','_','+','=','?','/','~','`',';',':','>','reut']
    bodyDictionary = {} # {key: word, value: occur times}
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

# find each word freqency in all articles and the number of article it appears
def buildIntermediateData2AndWordsFreq(intermediateData1, wordsFreq, intermediateData2,IntermediateData3):
    for key in intermediateData1:
        words = intermediateData1[key][2]
        totalWords = 0
        for word in words:
            #build 2 and wordsFreq
            if word not in wordsFreq:
                wordsFreq[word] = words[word]
            else:
                wordsFreq[word] += words[word]
            if word not in intermediateData2:
                intermediateData2[word] = 1
            else:
                intermediateData2[word] += 1
            totalWords += words[word]

        IntermediateData3[key] = totalWords

# TF part
def calcTFForEachIntermediateData1(TF,intermediateData1,intermediateData3):
    for key in intermediateData1:
        TFDic = {}
        words = intermediateData1[key][2]
        TFValue = 0
        for word in words:
            totalWords = intermediateData3[key]
            TFValue = words[word]/(totalWords * 1.0)
            TFDic[word] = TFValue
        TF[key] = TFDic
# IDF part
def calcIDFForEachWord(IDF, totalNumber,intermediateData2):
    for word in intermediateData2:
        idfValue = math.log10((totalNumber*1.0)/(1+(intermediateData2[word]*1.0)))
        IDF[word] = idfValue

# TFIDF part
def buildTFIDFValueForEachArticle(TFIDF,TF,IDF):
    for article in TF:
        TFIDFForEachArticle = {}
        for word in TF[article]:
            TFIDFValue = TF[article][word] * IDF[word]
            TFIDFForEachArticle[word] = TFIDFValue
        TFIDF[article] = TFIDFForEachArticle

# Generate the feature vector
def buidFeatureVectorWay1(TFIDF):
    featureVec = []
    for article in TFIDF:
            sort={}
            sort = sorted(TFIDF[article].items(),key=lambda x:x[1], reverse=True)
            if len(sort)>=4:
                for x in range(0,4):
                    if sort[x][0] not in featureVec:

                        featureVec.append(sort[x][0])
    return featureVec

# output fv to a file
def printBasedOnVec(intermediateData1,vc):
    f1=open('vc1.txt', 'w+')
    num = len(vc)
    vcForEachArticle = []
    for word in vc:
        vcForEachArticle.append(0)
    for article in intermediateData1:
        #a = intermediateData1[article][2]
        for word in intermediateData1[article][2]:
            if word in vc:
                index = vc.index(word)
                vcForEachArticle[index] += 1
        #print intermediateData1[article][0]
        f1.write(article)
        f1.write(" | ")
        for i in range(0,len(vcForEachArticle)):
            f1.write(str(vcForEachArticle[i]))
            f1.write(" ")
        f1.write(" | ")
        for i in range(0,len(intermediateData1[article][0])):
            f1.write(intermediateData1[article][0][i])
            f1.write(" ")
        for i in range(0,len(intermediateData1[article][1])):
            f1.write(intermediateData1[article][1][i])
            f1.write(" ")
        f1.write('\n')

# out attributes to a file
def pritnAttributes(vc):
    f1=open('attributesChoice.txt', 'w+')
    for word in vc:
        f1.write(word)
        f1.write(" ")


# declare some data structure we need (no need for python, only for clearness)

# a dictionary structure, whose key is date of each article and value
# is a list structure {Date: [['topics'],['places'], [all the words in each article]]}
intermediateData1 = {}

# a dictionary structure, whose key is date of each word and value
# is the number of article contains that word. Used for calc IDF
intermediateData2 = {}

# used to calc tf
intermediateData3 = {}
# tf for each word in each article
TF = {}
IDF = {}
TFIDF ={}
wordsFreq = {}
# total number of articles
totalNumber = 0
# read all files in a directory
# ask user to type the path of data directory
path = raw_input("Please enter the path of the folder contain all the .sgm files\n(For example /Users/junwang/Desktop/DataMining/Project1/TestDataset/): \n")
#path = '/Users/junwang/Desktop/DataMining/Project1/TestDataset/'
#path = '/Users/junwang/Desktop/DataMining/Data/'
dir = os.listdir(path)
# iterate each article in each file
for file in dir:
    sgm = open(path + file).read()
    soup = BeautifulSoup(sgm,'html.parser')
    # processing raw data step 1: build intermediateData1
    totalNumber += buildingIntermediateData1(soup,intermediateData1,totalNumber)
print ('Building intermediateData1 done..')
buildIntermediateData2AndWordsFreq(intermediateData1,wordsFreq,intermediateData2,intermediateData3)
print ('Building intermediateData2 done..')
calcTFForEachIntermediateData1(TF,intermediateData1,intermediateData3)
calcIDFForEachWord(IDF,totalNumber,intermediateData2)
buildTFIDFValueForEachArticle(TFIDF,TF,IDF)
print ('Calculate TFIDF done..')
v1 = buidFeatureVectorWay1(TFIDF)
printBasedOnVec(intermediateData1,v1)
pritnAttributes(v1)
print ('Done')
