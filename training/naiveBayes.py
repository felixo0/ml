#MAC OS X, Python3.5
#2016.1.15
#mangobada@163.com
'''
a simple implement of naive Bayes model
'''
import re
import random
import operator
import feedparser
import numpy as np

#a simple data set to verify the correction of algorithms
def load_data_set():
    posting_list=[['my', 'dog', 'has', 'flea', \
                          'problems', 'help', 'please'],
                         ['maybe', 'not', 'take', 'him', \
                          'to', 'dog', 'park', 'stupid'],
                         ['my', 'dalmation', 'is', 'so', 'cute', \
                           'I', 'love', 'him'],
                         ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                         ['mr', 'licks', 'ate', 'my', 'steak', 'how',\
                           'to', 'stop', 'him'],
                         ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vector=[0,1,0,1,0,1] #1 is negtive
    return posting_list,class_vector

#preprocess  data set
def pre_process(data_set):
    #cunstom pre_process function to porduce applicapble data set
    return data_set

#create vocabulary of of the whole data set
def create_lexicon_list(data_set):
    lexicon_set=set([])
    for doc in data_set:
        lexicon_set=lexicon_set | set(doc)
    return list(lexicon_set) 

#transform the words list to vector, 1 is exist, 0 is not
def words_to_vec(lexicon_list,input_set):
    vector=[0]*len(lexicon_list)
    for word in input_set:
        if word in lexicon_list:
            result[lexicon_list.index(word)]=1
        else:
            print('the word %s is not in lexicon' %word)
    return vector

#another way to transform words list to vector, 
#the number in result express the times word appears
def words_to_vec_count(lexicon_list,input_set):
    vector=[0]*len(lexicon_list)
    for word in input_set:
        if word in lexicon_list:
            result[lexicon_list.index(word)]+=1
        else:
            print('the word %s is not in lexicon' %word)
    return vector

#train model by sample matirx and class label
def train(train_matrix,train_category):
    num_of_sample=len(train_matrix)
    len_of_sample=len(train_matrix[0])
    num_abusive=0
    for label  in  train_category:
        if label==1:
            num_abusive+=1
    prob_abusive=num_abusive/len(train_category)
    prob_0_nume=np.ones(len_of_sample)
    prob_1_nume=np.ones(len_of_sample)
    prob_0_denom=2.0
    prob_1_denom=2.0
    for i in range(num_of_sample):
        if train_category[i]==0:
            prob_0_nume+=train_matrix[i]
            prob_0_denom+=sum(train_matrix[i])
        else:
            prob_1_nume+=train_matrix[i]
            prob_1_denom+=sum(train_matrix[i])
    prob_0_vec=np.log(prob_0_nume/prob_0_denom)
    prob_1_vec=np.log(prob_1_nume/prob_1_denom)
    return prob_0_vec, prob_1_vec, prob_abusive

#classify the input_vec based on the model
def classify(input_vec, prob_0_vec, prob_1_vec, prob_abusive):
    p0=sum(input_vec*prob_0_vec)+np.log(1-prob_abusive)
    p1=sum(input_vec*prob_1_vec)+np.log(prob_abusive)
    if p1>p0:
        return 1
    else:
        return 0

def text_parse(text):
    tokens=re.split(r'\W*',text)
    tokens=[token.lower() for token in tokens if len(token)>2]
    return tokens

#
def test(test_matrix):
    pass

#test the correction of the model on a small data set
def temp_test():
    posts,classes=load_data_set()
    lexicon=create_lexicon_list(posts)
    train_matrix=[]
    for post in posts:
        train_matrix.append(words_to_vec(lexicon,post))
        p0,p1,p_abusive=train(train_matrix,classes)
    #test_entry = ['love', 'my', 'dalmation']
    #doc_1 = np.array(words_to_vec(lexicon, test_entry))
    #print(test_entry,'classified as: ',classify(doc_1,p0,p1,p_abusive)) 
    test_entry_2 = ['stupid', 'garbage']
    doc_2 = np.array(words_to_vec(lexicon, test_entry_2))
    print(test_entry_2,'classified as: ',classify(doc_2,p0,p1,p_abusive))

#
def spam_test():
    docs=[]; class_labels = []; full_text =[]
    for i in range(1,26):
        word_list = text_parse(open('dataSet/Ch04/email/spam/%d.txt' %i).read())
        docs.append(word_list)
        full_text.extend(word_list)
        class_labels.append(1)
        word_list = text_parse(open('dataSet/Ch04/email/ham/%d.txt' %i).read())
        docs.append(word_list)
        full_text.extend(word_list)
        class_labels.append(0)
    lexicon = create_lexicon_list(docs)
    training_set = list(range(50))
    test_set=[]
    #10 test, 40 train
    for i in range(10):
        rand_index = int(random.uniform(0,len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat=[]
    train_classes = []
    for doc_index in training_set:
        train_mat.append(words_to_vec_count(lexicon, docs[doc_index]))
        train_classes.append(class_labels[doc_index])
        p0_vec,p1_vec,p_spam = train(np.array(train_mat),np.array(train_classes)) 
    error_count = 0
    for doc_index in test_set:
        word_vec = words_to_vec_count(lexicon, docs[doc_index])
        if classify(np.array(word_vec),p0_vec,p1_vec,p_spam) !=class_labels[doc_index]:
            error_count += 1
    print('the error rate is: ',float(error_count)/len(test_set))

#
def get_frequence(lexicon,text):
    freq_dict = {}
    for token in lexicon:
    freq_dict[token]=text.count(token)
    sorted_freq = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_freq[:30]

#
def localWords(feed1,feed0):
docList=[]; classList = []; fullText =[]
minLen = min(len(feed1['entries']),len(feed0['entries'])) for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:
           trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != \
            classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True) 
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**")
    for item in sortedSF:
        print(item[0])
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True) 
    print("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**") 
    for item in sortedNY:
        print(item[0])
