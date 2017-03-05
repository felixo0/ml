#it's a simple implementation of svm 
#drop the section of heuristic select alpha
#mangobada@163.com
#2016.2.10

import numpy as np
import random
'''

'''
def load_data(filename):
    matrix=[]
    class_labels=[]
    feature_names=[]
    fr=open(filename,'r')
    #feature_names=fr.readline().split()[:-1]
    for line in fr.readlines():
        word_list=line.strip().split()
        matrix.append([float(word_list[0]), float(word_list[1])])
        class_labels.append(float(word_list[2]))
        #matrix.append([1.0,float(words_list[0]),float(words_list[1])])
        #class_labels.append(words_list[-1])
    return matrix,class_labels,feature_names

def select_random_j(i,m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j

def clip_alpha(alpha_j,L,H):
    if alpha_j>H:
        alpha_j=H
    if alpha_j<L:
        alpha_j=L
    return alpha_j

def smo_simple(data_matrix,class_labels, C, toler, max_iter):
    data=np.mat(data_matrix)
    labels=np.mat(class_labels).transpose()
    b=0
    m,n=np.shape(data)
    alphas=np.mat(np.zeros((100,1)))
    iter=0
    while iter<max_iter:
        alpha_pairs_changed = 0
        for i in range(m):
            #fx=w.T*x+b, read details in paperi
            fxi=float(np.multiply(alphas,labels).T *(data*data[i,:].T))+b
            error_i=fxi-float(labels[i])
            t=labels[i] * error_i
            if (t<-toler and (alphas[i] < C))  or  (t > toler and (alphas[i] > 0)):
                j=select_random_j(i,m)
                fxj=float(np.multiply(alphas,labels).T * (data*data[j,:].T))+b
                error_j = fxj - float(labels[j])
                alpha_i_old=alphas[i].copy()
                alpha_j_old=alphas[j].copy()
                if labels[i] != labels[j]:
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C, C + alphas[j]-alphas[i])
                else:
                    L=max(0, alphas[j]+alphas[i]-C)
                    H=min(C, alphas[j]+alphas[i])
                if L==H:
                    print("L==H")
                    continue
                #eta is the optimal amount to change alpha[j]
                eta=2.0*data[i,:]*data[j,:].T - data[i,:]*data[i,:].T - data[j,:]*data[j,:].T
                if eta >= 0 :
                    print("eta>=0")
                    continue
                alphas[j] -= labels[j]*(error_i - error_j)/eta
                alphas[j] = clip_alpha(alphas[j], L, H)
                if abs(alphas[j] - alpha_j_old) < 0.00001:
                    print("j not moving enough")
                    continue
                alphas[i] += labels[j] * labels[i] * (alpha_j_old - alphas[j])
                b1 = b - error_i - labels[i] * (alphas[i]-alpha_i_old)* data[i,:]*data[i,:].T - \
                     labels[j]*(alphas[j]-alpha_j_old)*data[i,:]*data[j,:].T
                b2 = b - error_j - labels[i] * (alphas[i]-alpha_i_old)* data[i,:]*data[j,:].T - \
                     labels[j]*(alphas[j]-alpha_j_old)* data[j,:]*data[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): 
                    b = b2
                else: 
                    b = (b1 + b2)/2.0
                alpha_pairs_changed += 1
                print("iter: %d i:%d, pairs changed %d" %(iter,i,alpha_pairs_changed))
        if (alpha_pairs_changed == 0):
            iter += 1
        else:
            iter = 0
        print("iteration number: %d" % iter)
    return b,alphas
