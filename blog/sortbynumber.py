'''
Created on Feb 2, 2017
sort all the posts based on the popularity of their research topics

@author: Zhongchao
'''

from bson import ObjectId
from models import *
from .myChoices import *

def sort_post():
    dict = {}
    posts = Post.objects.all()
    for post in posts:
        for key in post.tags:
            if key in dict.keys():
                dict[key] = dict[key] + 1
            else:
                dict[key] = 1
    for post in posts:
        max_val = 0
        for key in post.tags:
            if (dict[key] > max_val):
                max_val = dict[key] 
        post.maxnumber = max_val
        post.save()
    
    posts = posts.all().order_by('-maxnumber')
    for post in posts:
        post.save()
        
    return posts