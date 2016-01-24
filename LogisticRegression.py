#Mac OS X python3.5
#20161.18
#mangobada@163.com

import numpy as np
import matplotlib.pyplot as plt
import random
'''
a simple implement of Logistic Regression
'''
#assume the first line is feature name,
#last column is class label
def load_data(filename):
    matrix=[]
    class_labels=[]
    feature_names=[]
    fr=open(filename,'r')
    #feature_names=fr.readline().split()[:-1]
    for line in fr.readlines():
        word_list=line.strip().split()
        matrix.append(word_list[:22])
        class_labels.append(word_list[22])
        #matrix.append([1.0,float(words_list[0]),float(words_list[1])])
        #class_labels.append(words_list[-1])
    return matrix,class_labels,feature_names

#if label is missing. delete that row, if there is a missing value in matrix, set it to 0
def pre_process(matrix,labels,features):
    new_matrix=[]
    new_labels=[]
    for i in range(len(matrix)):
        try:
            new_labels.append(float(labels[i]))
        except:
            continue
        else:
            for j in range(len(matrix[i])):
                try:
                    matrix[i][j]=float(matrix[i][j])
                except:
                    matrix[i][j]=0.0
            new_matrix.append(matrix[i])
    return new_matrix,new_labels,features

#sigmoid funtion
def sigmoid(x):
    return 1.0/(1+np.exp(-x))

#
def batch_gradient_ascent(data_matrix,class_labels,max_loop):
    matrix=np.mat(data_matrix,dtype=float)
    labels=np.mat(class_labels,dtype=float).transpose()
    m,n=np.shape(matrix)  #rows and cols of matrix
    alpha=0.001  #learning rate
    weights=np.ones((n,1),dtype=float)
    for i in range(max_loop):
        h=np.mat(sigmoid(matrix*weights))
        error=labels-h       #error is a column vector
        #eauql to w=w+aloha*(y-h(x))*x       function y=h(x), w is parameter
        weights = weights + alpha * matrix.transpose() * error
    return weights 

#
def stochastic_gradient_ascent(data_matrix, class_labels, max_iter):
    matrix=np.array(data_matrix,dtype=float)
    labels=np.array(class_labels,dtype=float)
    m,n=np.shape(matrix)
    weights=np.ones(n,dtype=float)
    for i in range(max_iter):
        data_index=list(range(m))
        for j in range(m):
            alpha=1.0/(i+j+1.0)+0.01
            random_index=int(random.uniform(0,len(data_index)))
            error=labels[random_index]-sigmoid(sum(matrix[random_index]*weights))
            weights=weights+alpha*matrix[random_index]*error
            del data_index[random_index]
    print(weights)
    return weights

#
def classify(X,weights):
    prob =sigmoid(sum(X*weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0

#
def test():
    train_data,train_labels,train_features=load_data('./dataset/horse-colic.data.txt')
    train_data,train_labels,train_features=pre_process(train_data,train_labels,train_features)
    weights=stochastic_gradient_ascent(train_data,train_labels,300)
    test_data,test_labels,test_features=load_data('./dataset/horse-colic.test.txt')
    test_data,test_labels,test_features=pre_process(test_data,test_labels,test_features)
    error_count=0.0
    all_count=len(test_data)
    for i in range(all_count):
        prob=classify(test_data[i],weights)
        if int(prob) !=int(test_labels[i]):
            error_count+=1
    error_rate= error_count/all_count
    print(all_count,error_count)
    return error_rate

#
def multi_test(iter_num):
    sum_error=0.0
    for i in range(iter_num):
        sum_error+=test()
        print(sum_error/(i+1))
    print(sum_error/iter_num)
    return sum_error/iter_num

#
def plot_fit(parameters):
    data_matrix,labels,feature_names=file_to_matrix('./dataset/Ch05/testSet.txt')
    data_array = np.array(data_matrix)
    n = np.shape(data_array)[0]
    x_1 = []; y_1 = []
    x_2 = []; y_2 = []
    for i in range(n):
        if int(labels[i])== 1:
            x_1.append(data_array[i,1]); y_1.append(data_array[i,2])
        else:
            x_2.append(data_array[i,1]); y_2.append(data_array[i,2])
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.scatter(x_1, y_1, s=30, c='red', marker='s') 
    ax.scatter(x_2, y_2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-para[0]-para[1]*x)/para[2]
    ax.plot(x, y)
    plt.xlabel('X1'); 
    plt.ylabel('X2');
    plt.show()
