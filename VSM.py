# BismiAllahirRahmaanirRaheem

import re, os, time, pickle, math, operator
from pprint import pprint

def fetchCollection(stopWords):
    terms = []
    docId = {}
    index = {}
    stats = {}
    termDict = {}
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
                            tempTerms.setdefault(word[0], 1)
                            index.setdefault(word[0], []).append(docId[story])
                        else:
                            tempTerms[word[0]] = tempTerms[word[0]]+1

        termDict.setdefault(docId[story], tempTerms)
        stats.setdefault(docId[story], len(tempTerms.keys()))

    index = dict(sorted(index.items()))
    return index, collecCount,stats, termDict


def buildVectors(index, termDict):
    vec = {}
    
    for i in termDict.keys():
        for term in index.keys():
            if term in termDict[i]:
                vec.setdefault(i, {}).setdefault(term,(termDict[i][term])*math.log10(len(termDict.keys())/(len(index[term]))))
            else:
                vec.setdefault(i, {}).setdefault(term,0)

    return vec

if __name__ == '__main__':

    print("\n------------Ad-Hoc Retrieval via Inverted Index-----------\n(Assumptions: Pre-processing removes all "
    "punctuation marks, stop words, repeated words & split the words like drawing-room into drawing & room)\n\n ***Statistics about Collection***")

    stopWords = ['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no']

    if not os.path.exists('inverted.pickle'):
        start = time.clock()
        index, T, stats, termDict = fetchCollection(stopWords)
        print("Corpus loaded from files  in: %.3f seconds" % (time.clock() - start))
        # writing VSM to file
        out = open("inverted.pickle", "wb")
        pickle.dump(index, out)
        out.close()
        out = open("inverted1.pickle", "wb")
        pickle.dump(termDict, out)
        out.close()
        print('Tokens in Collection (T):', T)
        print('Applying HEAP\'s Law with k = 34 and b = 0.49,\nwe get M ~ ', int(34.0 * (T ** 0.49)))
        print('Actual terms in Collection (M):', len(index.keys()))
        print('Smallest document w.r.t No. of terms: ', min(stats, key=stats.get),'.txt'
              '\nLargest document w.r.t No. of terms: ', max(stats, key=stats.get),'.txt'
              '\nAverage No. of terms per Document', sum(stats.values()) / 50)
    else:
        start = time.clock()
        fetch = open("inverted.pickle", "rb")
        index = pickle.load(fetch)
        fetch = open("inverted1.pickle", "rb")
        termDict = pickle.load(fetch)

        print("Corpus loaded from dump file in: %.3f seconds" % (time.clock() - start))

    # pprint(termDict)
    start = time.clock()
    vec = buildVectors(index, termDict)
    print("VSA established in: %.3f seconds" % (time.clock() - start))
    choice = ''
    while choice != 'exit' and choice != 'EXIT':
        # Query processing
        qToken = {}
        print('Enter 1 to start or \'exit\' to terminate program')
        choice = input('>>')
        if choice == '1':
            print("Enter free text query")
            query = input('>>')
            # query Parsing

            start = time.clock()
            qList = list(filter(None, re.split("[, \!?:_]+", query.casefold())))
            # calculating tf as well
            for q in qList:
                q = re.findall(r'[a-zA-Z0-9]+', q)
                q = q[0]
                if q and q not in stopWords:
                    if q not in qToken.keys():
                        qToken.setdefault(q,1)
                    else: qToken[q] = qToken[q]+1

            qVec = {}
            # whole query vector + tf*idf calc.
            for term in index.keys():
                if term in qToken.keys():
                    qVec[term] = qToken[term]*(math.log10(len(termDict.keys())/(len(index[term]))))
                else: qVec.setdefault(term, 0)

            # Cosine Similarity calc.
            qMag = 0
            result = {}

            for key in qVec:
                qMag += qVec[key] ** 2

            for i in range(1,len(vec)+1):
                vMag = 0
                dot = 0
                for key in vec[str(i)]:
                    dot += (vec[str(i)][key])*qVec[key]
                    vMag += (vec[str(i)][key]) ** 2

                result.setdefault(str(i), dot/(math.sqrt(qMag)*math.sqrt(vMag)))
            # pprint(result.items())
            # applying threshold
            result = dict((k,v) for k, v in result.items() if v >= 0.005)
            ordered =dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))

            print('Retrieved ',len(ordered), 'documents in %.3f seconds' % (time.clock() - start))
            print( ',\n'.join(
                ["'Doc. {}.txt': {}".format(k, v) for k, v in ordered.items()]
            ) )

        elif choice == 'exit' or choice == 'EXIT':
            print('Program terminated')
        else: print('Kindly, Enter correct input')