'''
Created on Feb 28, 2017
Search posts with the inputed keyword

@author: Zhongchao
'''

from bson import ObjectId
from models import *

'''
    search posts with the keyword, return all the posts if no keyword inputed
'''
def search_posts(searchresult):
    kw = searchresult.split(' ')
    if (len(kw) == 0):
        posts = Post.objects.all()
    elif (len(kw) > 0):
        posts = Post.objects.filter(title__icontains = kw[0])

    dict = {}
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