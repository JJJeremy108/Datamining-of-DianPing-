#_*_ coding:utf-8_*_

#Weibo sentiment analysis based on machine learning
from __future__ import print_function
from  gensim.models.word2vec import Word2Vec
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation  
from sklearn.metrics import classification_report
import  sys
reload(sys)
import  numpy as np
from  sklearn.preprocessing import scale
from  sklearn import svm
from sklearn.externals import joblib
import matplotlib.pyplot as plt

#Read the data from datafile
def loaddata():
	with open("data/pos.txt", "r") as pos_input:
		pos_weibo = pos_input.readlines()

	with open("data/neg.txt", "r") as neg_input:
		neg_weibo = neg_input.readlines()

	#Labled each sentence(1 for positive and 0 for negtive)and split them to train_data and test_data
	y =np.concatenate((np.ones(len(pos_weibo)), np.zeros(len(neg_weibo))))
	x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_weibo, neg_weibo)), y, test_size=0.2)
	return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = 	loaddata()

# train word2vec model
print ("loading word2vec corpus for training")
with open("data/corpus.txt", "r") as corpus_input:
	corpus = corpus_input.readlines()

# train word2vec model
print ("word2vec trainning processing")
n_dim = 300
imdb_w2v = Word2Vec(size=n_dim, min_count=10)
imdb_w2v.build_vocab(corpus)
imdb_w2v.train(x_train,total_examples=len(x_train), epochs=5)
imdb_w2v.train(x_test,total_examples=len(x_test), epochs=5)

def buildWordVector(text, size):
    vec = np.zeros(size).reshape((1, size))
    count =0
    for word in text:
        try:
            vec += imdb_w2v[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return  vec

train_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_train])
print (train_vecs.shape)
train_vecs =scale(train_vecs)
test_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_test])
print (test_vecs.shape)
imdb_w2v.save('w2v_model/w2v_model.pkl')
test_vecs = scale(test_vecs)

#training svm model
print('begin training svm model')
svm = svm.SVC(kernel='rbf',gamma= 0.001, C = 1000)
svm.fit(train_vecs,y_train)
joblib.dump(svm, 'model/svmmodel.pkl')
print(svm.score(test_vecs,y_test))
y_true, y_pred = y_test, svm.predict(test_vecs)  
print(classification_report(y_true, y_pred))  



