#Python3.5 Mac OS X
#2015.12.12

'''
implement of decision tree 
by ID3
'''

from math import log
import operator
import pickle

#calculate entropy
def entropy(dataSet):
    l=len(dataSet)
    labels={}
    for featureVec in dataSet:
        label=featureVec[-1]
        if label not in labels.keys():
            labels[label]=0
        labels[label]+=1
    entropy=0.0
    for item  in labels:
        prob=labels[item]/l
        entropy-=prob*log(prob,2)

    return entropy

#a small data set to test program
def createDataSet():
    dataSet = [[1, 1, 'yes'],
    [1, 1, 'yes'],
    [1, 0, 'no'],
    [0, 1, 'no'],
    [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels 

#return the splitted dataSet where feature equal to value
def splitDataSet(dataSet,featureAxis,value):
    result=[]
    for featureVec in dataSet:
        if featureVec[featureAxis]==value:
            reducedVec=featureVec[:featureAxis]
            reducedVec.extend(featureVec[featureAxis+1:])
            result.append(reducedVec)
    return result

#the best feature is the one that has largest infoGain
def chooseBestFeatureToSplit(dataSet):
    baseEntropy=entropy(dataSet)
    numOfFeatures=len(dataSet[0])-1
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numOfFeatures):
        featureValues=[x[i] for x in dataSet]
        uniqueFeatVal=set(featureValues)
        newEntropy=0.0
        for value in uniqueFeatVal:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/len(dataSet)
            newEntropy+=prob*entropy(subDataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature 

#get the majority count label of a set to represent the set
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0 ]

#recursively create a tree based on entropy
def createTree(dataSet,labels):
    classList=[x[-1] for x in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majority(classList)
    bestFeature=chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel=labels[bestFeature]
    myTree = {bestFeatureLabel:{}}
    del(labels[bestFeature])
    featValues = [example[bestFeature] for example in dataSet] 
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value),subLabels)
     return myTree

#classify the test sample by the input tree
def classify(inputTree,featureNames,test):
    firstKey=list(inputTree.keys())[0]
    secondDict=inputTree[firstKey]
    #print(firstKey)
    #print(featureNames)
    featureIndex=featureNames.index(firstKey)
    for key in secondDict.keys():
        if test[featureIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel= classify(secondDict[key],featureNames,test)
            else:
                classLabel=secondDict[key]
    return classLabel

#store the tree as a file
def storeTree(inputTree,filename):
    fw=open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()

#get tree from file
def getTree(filename):
    fr=open(filename,'rb')
    tree=pickle.load(fr)
    return tree

#based on inputTree and features, classify tests and compare the result with classLabels
def test(inputTree,features,tests,classLabels):
    errorCount=0
    numOfTests=len(tests)
    for i in range(numOfTests):
        result=classify(inputTree,features,test[i])
        if result!=classLabels[i]:
            errorCount+=1
    errorRate=errorCount/numOfTests
    return errorRate
