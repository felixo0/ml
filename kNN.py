
import operator
import numpy as np
import os

def createDataSet():
	group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels=['A','A','B','B']
	return group,labels

#k nearest neighbor, where inX is the data wait for classfy, dataSet is trainning example
# labels is the label of the dataSet ,k is the number of nearest neighbors to voting
def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    #tile is a function in numpy, to make inX has same length with dataSet
    diffMat=np.tile(inX, (dataSetSize,1))-dataSet
    #use euclide distance,
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistances=distances.argsort()
    classCount={}
    for i in range(k):
        voteLabel=labels[sortedDistances[i]]
        classCount[voteLabel]=classCount.get(voteLabel,0)+1
    sortedClassCount=sorted(classCount.items(), key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#transform the text file to matrix
def file2matrix(filename):
    fr=open(filename)
    numberOfLines=len(fr.readlines())
    returnMat=np.zeros((numberOfLines,3))
    classLabelVector=[]
    fr=open(filename)
    index=0
    for line in fr.readlines():
        line=line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(listFromLine[-1])
        index+=1
    return returnMat,classLabelVector

#normalize the data
#new=(old-min)/(max-min)
def autoNorm(dataSet):
    minValue=dataSet.min(0)
    maxValue=dataSet.max(0)
    ranges=maxValue-minValue
    normDataSet=np.zeros(np.shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-np.tile(minValue,(m,1))
    normDataSet=normDataSet/np.tile(ranges,(m,1))
    return normDataSet, ranges, minValue

#test 
def datingClassTest():
    testTrainRatio=0.1
    datingMat,labels=file2matrix('datingTestSet2.txt')
    normDataSet,ranges,minValue=autoNorm(datingMat)
    m=normDataSet.shape[0]
    numOfTest=int(m*testTrainRatio)
    errorCount=0.0
    for i in range(numOfTest):
        #choose the first 10% as test example, others as trainning dataset
        result=classify0(normDataSet[i,:],normDataSet[numOfTest:m,:],labels[numOfTest:m],3)
        print("the classifier come with %d, the real answer is %d" %(int(result),int(labels[i])))
        if int(result)!=int(labels[i]):
            errorCount+=1.0
    print(errorCount)
    errorRate=errorCount/numOfTest
    print("the error rate is %f" %errorRate)

#classify a new person input by user
def classifyPerson():
    resultList = ['not at all','in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games?")) 
    ffMiles = float(input("frequent flier miles earned per year?")) 
    iceCream = float(input("liters of ice cream consumed per year?")) 
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt') 
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = np.array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("You will probably like this person: ",resultList[int(classifierResult) - 1])

def image2Vec(filename):
    resultVec=np.zeros((1,1024))
    fr=open(filename,'r')
    
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            resultVec[0,32*i+j]=lineStr[j]
    fr.close()
    return resultVec

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('trainingDigits') 
    m = len(trainingFileList)
    trainingMat = np.zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = image2Vec('trainingDigits/%s'  %fileNameStr)
    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = image2Vec('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d"% (classifierResult, classNumStr))
        if (classifierResult != classNumStr):
            errorCount += 1.0
        print("\nthe total number of errors is: %d" % errorCount)
        print("\nthe total error rate is: %f" % (errorCount/float(mTest)))

