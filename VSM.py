# BismiAllahirRahmaanirRaheem
import re, os, time, pickle, math
from pprint import pprint

def fetchCollection():
    stopWords = ['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no']
    terms = []
    docId = {}
    index = {}
    termDict = {}
    ifidfDict = {}
    path = 'ShortStories'
    tokenCount = 0
    collecCount = 0
    
    for filename in os.listdir(path):
        collecFile = open(os.path.join('ShortStories',filename), 'r')
        story = collecFile.readline()
        author = collecFile.readline()
        author = author.replace('by','')
        docId.setdefault(story,filename.strip('.txt'))
        # print(story, author)
        tempTerms = {}
        # filename =
        for i, line in enumerate(collecFile):
            if i > 0:
                line = filter(None, re.split("[, \-!?:_]+", line))
                for word in line:
                    collecCount += 1
                    word = re.findall(r'[\w]+', word.casefold())
                    if word and word[0] not in stopWords:
                        tokenCount += 1
                        terms.append(word[0])
                        if word[0] not in tempTerms.keys():
                            tempTerms.setdefault(word[0],1)
                            index.setdefault(word[0], []).append(docId[story])
                        else:
                            tempTerms[word[0]] = tempTerms[word[0]]+1

        termDict.setdefault(docId[story], tempTerms)

    index = dict(sorted(index.items()))
    return index,termDict

def buildVectors(index,termDict):
    vec = {}
    idf = {}

    for i in termDict.keys():
        for term in index.keys():
            if term in termDict[i]:
                vec.setdefault('doc'+i, {}).setdefault(term,(termDict[i][term])*math.log10(len(termDict.keys())//(len(index[term]))))
            else:
                vec.setdefault('doc'+i, {}).setdefault(term,0)

    return vec

if __name__ == '__main__':

    print("\n------------Ad-Hoc Retrieval via Inverted Index-----------\n(Assumptions: Pre-processing removes all "
    "punctuation marks, stop words, repeated words & split the words like drawing-room into drawing & room)\n\n ***Statistics about Collection***")

    start = time.clock()
    index,termDict = fetchCollection()
    print("Dimensions for vectors calculated in: %.3f seconds" % (time.clock() - start))
    
    size = len(index.keys())
    print("charya horha he")
    # pprint((termDict['31']))
    start = time.clock()
    vec = buildVectors(index,termDict)
    print("VSA established in: %.3f seconds" % (time.clock() - start))
    pprint((vec['doc31']))
    print((termDict['31']['children']))
    print(len(index['children']))
    print((termDict['31']['children']) * math.log10(len(termDict.keys()) // (len(index['children']))))