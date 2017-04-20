'''
Created on Feb 6, 2017
add or narrow down research topics

@author: Zhongchao
'''

from bson import ObjectId
from models import *
from .myChoices import *
from createPost import find_topic

'''
    reset topics to default settings
'''
def resettopic():
    Dropdown.objects.all().delete()
    TopicList.objects.all().delete()
    for cat in Category:
        Dropdown.objects.create(title = cat[0])
        for t in Topic[cat[0]]:
            TopicList.objects.create(category = cat[0], topic = t[0], value = t[1])


'''
    add new topics
'''        
def addtopic(category, topic, value):
    print category, topic, value
    if (len(TopicList.objects.filter(category = category)) > 0):
        TopicList.objects.create(category = category, topic = topic, value = value)
        

'''
    narrow down topics
'''        
def selecttopic(category, topics):
    TopicList.objects.filter(category = category).delete()
    for topic in topics:
        tag = find_topic(category, topic)
        TopicList.objects.create(category = category, topic = tag, value = topic)
    
    
    