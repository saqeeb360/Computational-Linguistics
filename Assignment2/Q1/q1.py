# -*- coding: utf-8 -*-
from io import open
# from conllu import parse

with open("hindi.conllu", 'r') as file:
    temp = file.read()

from collections import defaultdict
import itertools
from collections import Counter

"""**Solution 1a**"""
print("----------Solution 1a------------")
def freqPOSword(parseText):
  posTag = defaultdict(int)
  for sentence in parseText:
    for word in sentence:
      # posTag[(word['upos'],word['form'])] += 1
      posTag[word['upos']] += 1
  posTag = dict(sorted(posTag.items(), key=lambda item: item[1] ,reverse=True))
  # return dict(itertools.islice(posTag.items(), 50))
  return posTag

parseText = parse(temp)
posTag = freqPOSword(parseText)
print(posTag)

"""**Solution 1b**"""
print("----------Solution 1b------------")
def freq50Pos():
  freq50most = dict()
  for sentence in parseText:
    for word in sentence:
      wordlist = freq50most.get(word['upos'],[])
      wordlist.append(word['form'])
      freq50most[word['upos']] = wordlist

  finaldict = dict()
  for key, wordlist in freq50most.items():
    posWord = dict(Counter(wordlist))
    posWord =  dict(sorted(posWord.items(), key=lambda item: item[1] ,reverse=True))
    posWord = dict(itertools.islice(posWord.items(), 50))
    finaldict[key] = posWord
    print(key, posWord)
  return finaldict

freq50mostdict = freq50Pos()

"""**Solution 1c** """
print("----------Solution 1c------------")
def findfreqGender(morphfeature):
  genderfreq = defaultdict(int)
  for sentence in parseText:
    for word in sentence:
      featdict = word.get('feats')
      if featdict != None:
        genstr = featdict.get(morphfeature,'')
        if genstr != '':
          genderfreq[genstr] += 1
  return genderfreq

genderfreq = findfreqGender('Gender')
print('-------Gender--------')
for key, value in genderfreq.items():
  print(key, value)
genderfreq = findfreqGender('Case')
print('\n-------Case----------')
for key, value in genderfreq.items():
  print(key, value)
print('\n-------Number--------')
genderfreq = findfreqGender('Number')
for key, value in genderfreq.items():
  print(key, value)

#find freq of Gender, case, number of words 
def genFreq(morfeature):
  genderfreq = dict()
  for sentence in parseText:
    for word in sentence:
      featdict = word.get('feats')
      if featdict != None:
        genstr = featdict.get(morfeature,'')
        if genstr != '':
          genlist = genderfreq.get(genstr,[])
          genlist.append(word['form'])
          genderfreq[genstr] = genlist
  
  finalgenfreq = dict()
  for key, genlist in genderfreq.items():
    finalgenfreq[key] = dict(itertools.islice(dict(sorted(dict(Counter(genlist)).items(), key=lambda item: item[1] ,reverse=True)).items(),50))
  return finalgenfreq

genderfreq = genFreq('Gender')
for key, value in genderfreq.items():
  print(key, value)

casefreq = genFreq('Case')
for key, value in casefreq.items():
  print(key, value)

numberfreq = genFreq('Number')
for key, value in numberfreq.items():
  print(key, value)

"""**Solution 1d**"""
print("----------Solution 1d------------")
freq50Comb = defaultdict(int)

for sentence in parseText:
  for word in sentence:
    featdict = word.get('feats')
    if featdict != None:
      genstr = featdict.get('Gender','')
      casestr = featdict.get('Case','')
      numstr = featdict.get('Number','')
      if genstr != '' and casestr != '' and numstr != '':
        freq50Comb[(genstr, casestr, numstr)] += 1

freq50Comb = dict(sorted(dict(freq50Comb).items(), key=lambda item: item[1] ,reverse=True))
freq50Comb

"""**Solution 1e**"""
print("----------Solution 1e------------")

headdict = dict()

def POShead():
  headdict = dict()
  for sentence in parseText:
    for word in sentence:
      if word['misc']['ChunkType'] == 'head':
        headlist = headdict.get(word['upos'], [])
        headlist.append(word['form'])
        headdict[word['upos']] = headlist

  finalheaddict = dict()
  for key, headlist in headdict.items():
    headCount = dict(sorted(dict(Counter(headlist)).items(), key=lambda item: item[1] ,reverse=True))
    finalheaddict[key] = headCount
    print(key, headCount)
  return finalheaddict

headdict = POShead()

"""**Solution 1f**"""
print("----------Solution 1f------------")

def getdirectedPOS():
  directedPOS = dict()
  # def getdirectedPOS():
  for sentence in parseText:
    for word in sentence:
      if word['head'] != 0:
        mytup = (word['upos'], sentence[word['head']-1]['upos'])
        # eachlist = directedPOS.get(word['deprel'], [])
        eachlist = directedPOS.get(mytup, [])
        eachlist.append(word['deprel'])
        directedPOS[mytup] = eachlist

  finaldirectedPOS = dict()
  for key,eachlist in directedPOS.items():
    eachCount = dict(sorted(dict(Counter(eachlist)).items(), key=lambda item: item[1] ,reverse=True))
    finaldirectedPOS[key] = eachCount
    print(key, eachCount)
  return finaldirectedPOS

directedPOS = getdirectedPOS()

# 1.f -> part 1
allTuples = list(directedPOS.keys())
print(allTuples)

totaldirectedPOS = defaultdict(int)

for key1, eachlist in directedPOS.items():
  for key2 , eachitem in eachlist.items():
    totaldirectedPOS[key1] += eachitem
  print(key1, totaldirectedPOS[key1])

"""**Solution 1g**"""
print("----------Solution 1g------------")

def dependencyR():
  directedPOS = dict()
  for sentence in parseText:
    for word in sentence:
      if word['head'] != 0:
        mytup = (word['upos'], sentence[word['head']-1]['upos'])
        eachlist = directedPOS.get(word['deprel'], [])
        eachlist.append(mytup)
        directedPOS[word['deprel']] = eachlist

  finaldirectedPOS = dict()
  for key,eachlist in directedPOS.items():
    eachCount = dict(sorted(dict(Counter(eachlist)).items(), key=lambda item: item[1] ,reverse=True))
    finaldirectedPOS[key] = eachCount
    print(key, eachCount)
  return finaldirectedPOS

dependencyRfreq = dependencyR()

depenRtotalfreq = defaultdict(int)

for key1, eachlist in dependencyRfreq.items():
  for key2 , eachitem in eachlist.items():
    depenRtotalfreq[key1] += eachitem
  print(key1, depenRtotalfreq[key1])

