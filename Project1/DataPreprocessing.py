__author__ = 'Po Yao'
__author__ = 'Jun wang'

import operator
import math
import os, sys
import nltk
from nltk.stem.lancaster import LancasterStemmer
from BeautifulSoup import BeautifulSoup
reload(sys)
sys.setdefaultencoding('Cp1252')
# functions go here
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

def buildingIntermediateData1(soup,intermediateData1,totalNumber):
    # iterate every article in the file
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
def calcTFForEachIntermediateData1(intermediateData1,intermediateData3):
    TFForEachArticle={}
    for key in intermediateData1:
        TFDic = {}
        words = intermediateData1[key][2]
        TFValue = 0;
        for word in words:
            totalWords = intermediateData3[key]
            TFValue = words[word]/(totalWords * 1.0)
            TFDic[word] = TFValue
        TFForEachArticle[key] = TFDic
    return TFForEachArticle

def calcIDFForEachWord(totalNumber,intermediateData2):
    IDF = {}
    for word in intermediateData2:
        idfValue = math.log10((totalNumber*1.0)/(1+(intermediateData2[word]*1.0)))
        IDF[word] = idfValue
    return  IDF
def buildTFIDFValueForEachArticle(TF,IDF):
    TFIDF = {}
    for article in TF:
        TFIDFForEachArticle = {}
        for word in TF[article]:
            TFIDFValue = TF[article][word] * IDF[word]
            TFIDFForEachArticle[word] = TFIDFValue
    TFIDF[article] = TFIDFForEachArticle
    return TFIDF
def buidFeatureVectorWay1(TFIDF):
    featureVec = []
    for article in TFIDF:
        sortedValue = sorted(TFIDF[article].values())
        num = len(sortedValue)
        max1 = sortedValue[num-1]
        max2 = sortedValue[num-2]
        max3 = sortedValue[num-3]
        attr1 = ''
        attr2 = ''
        attr3 = ''
        for word in TFIDF[article]:
            
            #print TFIDF[article][word]
            if (TFIDF[article][word] == max1 or TFIDF[article][word] == max2 or TFIDF[article][word] == max3) and (attr1 != ''):
                attri1 = word
            if (TFIDF[article][word] == max1 or TFIDF[article][word] == max2 or TFIDF[article][word] == max3) and (attr1 != ''):
                attri2 = word
            if (TFIDF[article][word] == max1 or TFIDF[article][word] == max2 or TFIDF[article][word] == max3) and (attr1 != ''):
                attri3 = word
        featureVec.append(attr1)
        featureVec.append(attr2)
        featureVec.append(attr3)
    return featureVec



# declare some data structure we need
# a dictionary structure, whose key is date of each article and value
# is a list structure {['topics'],['places'], [all the words in each article]}
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
totalNumber = 0
# read all files in a directory
# TO Do ask user to type the path of data directory
path = '/Users/junwang/Desktop/DataMining/Project1/TestDataset/'
#path = '/Users/junwang/Desktop/DataMining/Data/'
dir = os.listdir(path)
# iterate each article in each file
for file in dir:
    sgm = open(path + file).read()
    soup = BeautifulSoup(''.join(sgm))
    # processing raw data step 1: build intermediateData1
    totalNumber = buildingIntermediateData1(soup,intermediateData1,totalNumber)
    buildIntermediateData2AndWordsFreq(intermediateData1,wordsFreq,intermediateData2,intermediateData3)

TF = calcTFForEachIntermediateData1(intermediateData1,intermediateData3)
IDF = calcIDFForEachWord(totalNumber,intermediateData2)
TFIDF = buildTFIDFValueForEachArticle(TF,IDF)


featureVec1 = buidFeatureVectorWay1(TFIDF)
print featureVec1

