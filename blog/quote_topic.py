'''
Created on Feb 19, 2017
Preprocess the title and content, predict research topics using hierarchical classifiers

@author: Zhongchao
'''

import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import traceback
import sys
import re
import pickle
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import loadmodel
import numpy

class QuoteTopic(object):
    
    def __init__(self, title, text):
        self.title = title
        self.text = text
        
    
    def setParams(self, title, text):
        self.title = title
        self.text = text
    
    def removeUnicode(self, text):
        printable = set(string.printable)
        if isinstance(text, list):
            for v in text:
                if len(v) > 25:
                    text = filter(lambda x: x in printable, v)
                    break
        else:           
            text = filter(lambda x: x in printable, text)
            
        return text if not isinstance(text, list) else ''
    
    '''
        tokenizing
    '''   
    def tokenize(self, title, text):
        data = self.removeUnicode(title)
        data += " "
            
        data += self.removeUnicode(text)
        data = data.lower()
        #data = data.encode('utf-8').translate(None, string.punctuation)
            
        return nltk.word_tokenize(data)
    
    '''
        remove stop words and digits
    '''
    def removeStopWordsAndDigits(self, tokens):
        # stopwords_list = getFileContent(self.resource_path, "en-stopwords.txt")
        pattern = re.compile(r'\d+')
        return [w for w in tokens if not w in stopwords.words('english') if not pattern.search(w)]
    
    '''
        stemming using Porter
    '''
    def stemTokens(self, tokens, stemmer=None):
        if not stemmer:
            stemmer = PorterStemmer()
                
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed
    
    '''
        predict research topics
    '''
    def quote(self):
        threshold = 1
        topics = []
        max_p = 0
        scale = 2
        flag = True
        
        # tokenize
        tokens = self.tokenize(self.title, self.text)
        # remove stopwords
        tokens = self.removeStopWordsAndDigits(tokens)
        # stemming
        tokens = self.stemTokens(tokens)
        # join data
        xdata = []
        for i in tokens:
            xdata.append(i.encode('ascii'))
        xdata = ' '.join(xdata)        
        # vectorizer
        xtest = loadmodel.vectorizer.transform([xdata])
        # select the first k terms with highest scores
        xtest = loadmodel.ch2.transform(xtest)
        # predict a category
        xpred_category = loadmodel.clf.predict(xtest)
        # calculate the probability
        probs_category = loadmodel.clf._predict_proba_lr(xtest)
        
        # same operations for computer science
        xtest = loadmodel.vectorizer_cs.transform([xdata])
        xtest = loadmodel.ch2_cs.transform(xtest)
        xpred_cs = loadmodel.clf_cs.predict(xtest)
        probs_cs = loadmodel.clf_cs._predict_proba_lr(xtest)
        
        # same operations for life science I
        xtest = loadmodel.vectorizer_lsa.transform([xdata])
        xtest = loadmodel.ch2_lsa.transform(xtest)
        xpred_lsa = loadmodel.clf_lsa.predict(xtest)
        probs_lsa = loadmodel.clf_lsa._predict_proba_lr(xtest)
        
        # same operations for life science II
        xtest = loadmodel.vectorizer_lsb.transform([xdata])
        xtest = loadmodel.ch2_lsb.transform(xtest)
        xpred_lsb = loadmodel.clf_lsb.predict(xtest)
        probs_lsb = loadmodel.clf_lsb._predict_proba_lr(xtest)
        
        
        '''
            get all the topics whose probabilities are above threshold
            retrieved topics should be ranked in probability
            the prediction happens just in the most probable category, ignoring other categories
        '''
        if xpred_category == 'CS':
            '''
                predict topics for computer science
            '''
            cur_threshold = scale * threshold / float(loadmodel.clf_cs.classes_.size)
            while (flag):
                max_p = 0
                tmp_topic = []  
                for idx2 in range(0, len(loadmodel.clf_cs.classes_)):              
                    if probs_cs.item(idx2) > cur_threshold and loadmodel.clf_cs.classes_[idx2] not in topics and probs_cs.item(idx2) > max_p:
                        max_p = probs_cs.item(idx2)
                        tmp_topic = loadmodel.clf_cs.classes_[idx2]                    
                if max_p > cur_threshold:
                    topics.append(tmp_topic)
                elif (topics == []):
                    for idx2 in range(0, len(loadmodel.clf_cs.classes_)):
                        if probs_cs.item(idx2) > max_p:
                            max_p = probs_cs.item(idx2)
                            tmp_topic = loadmodel.clf_cs.classes_[idx2]
                    topics.append(tmp_topic)
                    flag = False
                else:
                    flag = False
        elif xpred_category == 'LSA':
            '''
                predict topics for life science I
            '''
            cur_threshold = scale * threshold / float(loadmodel.clf_lsa.classes_.size)
            while (flag):
                max_p = 0
                tmp_topic = [] 
                for idx2, t in enumerate(loadmodel.clf_lsa.classes_):                
                    if probs_lsa.item(idx2) > cur_threshold and loadmodel.clf_lsa.classes_[idx2] not in topics and probs_lsa.item(idx2) > max_p:
                        max_p = probs_lsa.item(idx2)
                        tmp_topic = loadmodel.clf_lsa.classes_[idx2]
                if max_p > cur_threshold:
                    topics.append(tmp_topic)
                elif (topics == []):
                    for idx2 in range(0, len(loadmodel.clf_lsa.classes_)):
                        if probs_lsa.item(idx2) > max_p:
                            max_p = probs_lsa.item(idx2)
                            tmp_topic = loadmodel.clf_lsa.classes_[idx2]
                    topics.append(tmp_topic)
                    flag = False
                else:
                    flag = False
        elif xpred_category == 'LSB':
            '''
                predict topics for life science II
            '''
            cur_threshold = scale * threshold / float(loadmodel.clf_lsb.classes_.size)
            while (flag):
                max_p = 0
                tmp_topic = [] 
                for idx2, t in enumerate(loadmodel.clf_lsb.classes_):                
                    if probs_lsb.item(idx2) > cur_threshold and loadmodel.clf_lsb.classes_[idx2] not in topics and probs_lsb.item(idx2) > max_p:
                        max_p = probs_lsb.item(idx2) 
                        tmp_topic = loadmodel.clf_lsb.classes_[idx2]    
                if max_p > cur_threshold:
                    topics.append(tmp_topic)
                elif (topics == []):
                    for idx2 in range(0, len(loadmodel.clf_lsb.classes_)):
                        if probs_lsb.item(idx2) > max_p:
                            max_p = probs_lsb.item(idx2)
                            tmp_topic = loadmodel.clf_lsb.classes_[idx2]
                    topics.append(tmp_topic)
                    flag = False
                else:
                    flag = False          

        return topics
        
        '''
        xpred_category = loadmodel.clf.predict([xdata])
        if (xpred_category == 'CS'):
            xpred_cs = loadmodel.clf_cs.predict([xdata])
            topic = xpred_cs
        elif (xpred_category == 'LSA'):
            xpred_lsa = loadmodel.clf_lsa.predict([xdata])
            topic = xpred_lsa
        elif (xpred_category == 'LSB'):    
            xpred_lsb = loadmodel.clf_lsb.predict([xdata])
            topic = xpred_lsb
        
        return topic
        '''
    
        
if __name__ == '__main__':
    title = 'Storage and retrieval of system log events using a structured schema based on message type transformation'
    text = 'Message types are semantic groupings of the free form messages in system log events. The message types that exist in a log file, if known, can be used in several log management and analysis tasks. In this work, we explore the use of message types as a schema definition for the storage and retrieval of messages in event logs. We show how message types can be used to impose structure on the unstructured content of event logs and how this structured representation can provide a usable index for searching the contents of the log file. As a side benefit, the structured representation that message types impose also leads to the removal of redundant information in the event logs that leads to space savings on disk.'
    
    tokens = tokenize(title, text)
    tokens = removeStopWordsAndDigits(tokens)
    tokens = stemTokens(tokens)
    xdata = []
    for i in tokens:
        xdata.append(i.encode('ascii'))
    xdata = ' '.join(xdata)

    

    clf = joblib.load('D:/course/Project/classifier/category_pipeline.pkl')   
    xpred_category = clf.predict([xdata])

    if (xpred_category == 'CS'):
        clf_cs = joblib.load('D:/course/Project/classifier/cs_pipeline.pkl')
        xpred_cs = clf_cs.predict([xdata])
        topic = xpred_cs
    elif (xpred_category == 'LSA'):
        clf_lsa = joblib.load('D:/course/Project/classifier/lsa_pipeline.pkl')
        xpred_lsa = clf_lsa.predict([xdata])
        topic = xpred_lsa
    elif (xpred_category == 'LSB'):    
        clf_lsb = joblib.load('D:/course/Project/classifier/lsb_pipeline.pkl')
        xpred_lsb = clf_lsb.predict([xdata])
        topic = xpred_lsb
    
    
    
    
    '''
    with open('D:/course/Project/classifier/category_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('D:/course/Project/classifier/category_KBest.pkl', 'rb') as f:
        ch2 = pickle.load(f)
    with open('D:/course/Project/classifier/category_classifier.pkl', 'rb') as f:
        clf = pickle.load(f)    
    
    xtest = vectorizer.transform([xdata])
    xtest = ch2.transform(xtest)
    xpred_category = clf.predict(xtest)
    probs_category = clf._predict_proba_lr(xtest)

    with open('D:/course/Project/classifier/CS_vectorizer.pkl', 'rb') as f:
        vectorizer_cs = pickle.load(f)
    with open('D:/course/Project/classifier/CS_KBest.pkl', 'rb') as f:
        ch2_cs = pickle.load(f)
    with open('D:/course/Project/classifier/CS_classifier.pkl', 'rb') as f:
        clf_cs = pickle.load(f)
        
    xtest = vectorizer_cs.transform([xdata])
    xtest = ch2_cs.transform(xtest)
    xpred_cs = clf_cs.predict(xtest)
    probs_cs = clf_cs._predict_proba_lr(xtest)

    with open('D:/course/Project/classifier/LSA_vectorizer.pkl', 'rb') as f:
        vectorizer_lsa = pickle.load(f)
    with open('D:/course/Project/classifier/LSA_KBest.pkl', 'rb') as f:
        ch2_lsa = pickle.load(f)
    with open('D:/course/Project/classifier/LSA_classifier.pkl', 'rb') as f:
        clf_lsa = pickle.load(f)
        
    xtest = vectorizer_lsa.transform([xdata])
    xtest = ch2_lsa.transform(xtest)
    xpred_lsa = clf_lsa.predict(xtest)
    probs_lsa = clf_lsa._predict_proba_lr(xtest)

    with open('D:/course/Project/classifier/LSB_vectorizer.pkl', 'rb') as f:
        vectorizer_lsb = pickle.load(f)
    with open('D:/course/Project/classifier/LSB_KBest.pkl', 'rb') as f:
        ch2_lsb = pickle.load(f)
    with open('D:/course/Project/classifier/LSB_classifier.pkl', 'rb') as f:
        clf_lsb = pickle.load(f)
        
    xtest = vectorizer_lsb.transform([xdata])
    xtest = ch2_lsb.transform(xtest)
    xpred_lsb = clf_lsb.predict(xtest)
    probs_lsb = clf_lsb._predict_proba_lr(xtest)
    '''
      
'''
pipe = Pipeline([('tfvec', vectorizer), ('kb', ch2), ('svm', clf)])    
joblib.dump(pipe, 'D:/course/Project/classifier/category_pipeline.pkl')
pipe_cs = Pipeline([('tfvec', vectorizer_cs), ('kb', ch2_cs), ('svm', clf_cs)])    
joblib.dump(pipe_cs, 'D:/course/Project/classifier/cs_pipeline.pkl')
pipe_lsa = Pipeline([('tfvec', vectorizer_lsa), ('kb', ch2_lsa), ('svm', clf_lsa)])    
joblib.dump(pipe_lsa, 'D:/course/Project/classifier/lsa_pipeline.pkl')
pipe_lsb = Pipeline([('tfvec', vectorizer_lsb), ('kb', ch2_lsb), ('svm', clf_lsb)])    
joblib.dump(pipe_lsb, 'D:/course/Project/classifier/lsb_pipeline.pkl')
'''
