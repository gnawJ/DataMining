__author__ = 'junwang'
# import nltk
# from BeautifulSoup import BeautifulSoup
# path = '/Users/junwang/Desktop/DataMining/Project1/TestDataset/reutTest1.sgm'
# sgm = open(path).read()
# soup = BeautifulSoup(''.join(sgm))
# bodies = soup.findAll('body')
# for body in bodies:
#     bodystring = str(body.next.string)
#     tokens = nltk.word_tokenize(bodystring,language='english')
#     print tokens
def checkOnlyContainNumAndComma(string):
    flag = True
    validSet = ['1','2','3','4','5','6','7','8','9','0',',']
    for c in string:
        if c not in validSet:
            return False
    return flag

a = '1000a'
print checkOnlyContainNumAndComma(a)