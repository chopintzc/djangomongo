'''
Created on Feb 23, 2017
Prepare json data for the D3 force-directed graph

@author: Zhongchao
'''


from models import *


def create_json(author, filter):
    j = {}
    nodes = []
    links = []
    groups = {}
    
    '''
        create nodes
        node is labeled by the group which is most prevalent in the dataset
    '''
    ids = Profile.objects.get(author = author).ids
    for id in ids:
        if (filter[0] == "none"):
            node = {}
            post = Post.objects.get(pk = id)
            node[unicode('id', "utf-8")] = post.title
            if post.tags[0] not in groups:
                length = len(groups)
                groups[post.tags[0]] = length
            node[unicode('group', "utf-8")] = groups[post.tags[0]]
            nodes.append(node)  
            '''  
            for idx, tag in enumerate(post.tags):
                if tag not in groups:
                    length = len(groups)
                    groups[tag] = length
                    node[unicode('group', "utf-8")] = groups[tag]
                    break
                if idx == len(post.tags)-1:
                    node[unicode('group', "utf-8")] = groups[tag]  
            nodes.append(node)           
            '''        
        else:
            post = Post.objects.get(pk = id)
            for f in post.tags:
                if (f in filter):
                    node = {}
                    node[unicode('id', "utf-8")] = post.title
                    '''
                    for idx, tag in enumerate(post.tags):
                        if tag not in groups and tag in filter:
                            length = len(groups)
                            groups[tag] = length
                            node[unicode('group', "utf-8")] = groups[tag]
                            break
                        if idx == len(post.tags) - 1:
                            node[unicode('group', "utf-8")] = groups[tag]
                    '''
                    if f not in groups:
                        length = len(groups)
                        groups[f] = length
                    node[unicode('group', "utf-8")] = groups[f]
                    nodes.append(node)
                    break
    
    
    '''
        create links
        link weight is related to the number of common topics
    '''            
    if (filter[0] == "none"):        
        for key, value in groups.iteritems(): 
            names = []           
            posts = Post.objects.filter(tags__exact = key, pk__in = ids)
            for p in posts:
                names.append(p.title)
            for p1 in range(0, len(names)-1):
                for p2 in range(p1+1, len(names)):
                    link = {}
                    link[unicode('source', "utf-8")] = names[p1]
                    link[unicode('target', "utf-8")] = names[p2]
                    link[unicode('value', "utf-8")] = 1
                    flag = False
                    for idx, lk in enumerate(links):
                        if ((lk[unicode('source', "utf-8")] == names[p1] and lk[unicode('target', "utf-8")] == names[p2]) or (lk[unicode('source', "utf-8")] == names[p2] and lk[unicode('target', "utf-8")] == names[p1])):
                            lk[unicode('value', "utf-8")] += 1
                            flag = True
                            break
                    if flag == False:
                        links.append(link)
    else:
        for f in filter:
            names = []
            posts = Post.objects.filter(tags__exact = f, pk__in = ids)
            for p in posts:
                names.append(p.title)
            for p1 in range(0, len(names)-1):
                for p2 in range(p1+1, len(names)):
                    link = {}
                    link[unicode('source', "utf-8")] = names[p1]
                    link[unicode('target', "utf-8")] = names[p2]
                    link[unicode('value', "utf-8")] = 1
                    flag = False
                    for idx, lk in enumerate(links):
                        if ((lk[unicode('source', "utf-8")] == names[p1] and lk[unicode('target', "utf-8")] == names[p2]) or (lk[unicode('source', "utf-8")] == names[p2] and lk[unicode('target', "utf-8")] == names[p1])):
                            lk[unicode('value', "utf-8")] += 1
                            flag = True
                            break
                    if flag == False:
                        links.append(link)
        
                
    j[unicode('nodes', "utf-8")] = nodes
    j[unicode('links', "utf-8")] = links
    return j