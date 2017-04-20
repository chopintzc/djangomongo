'''
Created on Feb 16, 2017
load the trained hierarchical classification model

@author: Zhongchao
'''

from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import pickle

def init():
    
    global vectorizer, ch2, clf, vectorizer_cs, ch2_cs, clf_cs, vectorizer_lsa, ch2_lsa, clf_lsa, vectorizer_lsb, ch2_lsb, clf_lsb
    
    # load the model for category classification
    with open('D:/course/Project/classifier/category_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('D:/course/Project/classifier/category_KBest.pkl', 'rb') as f:
        ch2 = pickle.load(f)
    with open('D:/course/Project/classifier/category_classifier.pkl', 'rb') as f:
        clf = pickle.load(f) 
    
    # load the model for Computer Science topic classification
    with open('D:/course/Project/classifier/CS_vectorizer.pkl', 'rb') as f:
        vectorizer_cs = pickle.load(f)
    with open('D:/course/Project/classifier/CS_KBest.pkl', 'rb') as f:
        ch2_cs = pickle.load(f)
    with open('D:/course/Project/classifier/CS_classifier.pkl', 'rb') as f:
        clf_cs = pickle.load(f)
    
    # load the model for Life Science I topic classification    
    with open('D:/course/Project/classifier/LSA_vectorizer.pkl', 'rb') as f:
        vectorizer_lsa = pickle.load(f)
    with open('D:/course/Project/classifier/LSA_KBest.pkl', 'rb') as f:
        ch2_lsa = pickle.load(f)
    with open('D:/course/Project/classifier/LSA_classifier.pkl', 'rb') as f:
        clf_lsa = pickle.load(f)
    
    # load the model for Life Science II topic classification     
    with open('D:/course/Project/classifier/LSB_vectorizer.pkl', 'rb') as f:
        vectorizer_lsb = pickle.load(f)
    with open('D:/course/Project/classifier/LSB_KBest.pkl', 'rb') as f:
        ch2_lsb = pickle.load(f)
    with open('D:/course/Project/classifier/LSB_classifier.pkl', 'rb') as f:
        clf_lsb = pickle.load(f)
    
    '''
    global clf, clf_cs, clf_lsa, clf_lsb
    clf = joblib.load('D:/course/Project/classifier/category_pipeline.pkl') 
    clf_cs = joblib.load('D:/course/Project/classifier/cs_pipeline.pkl')
    clf_lsa = joblib.load('D:/course/Project/classifier/lsa_pipeline.pkl')
    clf_lsb = joblib.load('D:/course/Project/classifier/lsb_pipeline.pkl')
    '''