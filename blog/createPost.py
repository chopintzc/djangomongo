'''
Created on Jan 25, 2017
create new post

@author: Zhongchao
'''

from models import *
from quote_topic import QuoteTopic
from myChoices import *

'''
    create a new post with title and content
    return the post id
'''
def create_new_post(title, text):
    
    quotetopic = QuoteTopic(title, text)
    topics = quotetopic.quote()
    tags = []
    for topic in topics:
        tag = find_tag(unicode(topic, "utf-8"))
        tags.append(tag)
    Post.objects.get(title = title).delete()
    post = Post.objects.create(title = title, text = text, is_published = True, tags = tags)
    return post.id
    '''
    except:
        print 'not able to upload file'
        post = Post.objects.get(title = title)
        return post.id
    '''   

      
def find_tag(topic):
    topics = TopicList.objects.filter(topic=topic)
    return str(topics[0].value)


def find_topic(category, val):
    for key, value in Topic.iteritems():
        if (key == category):
            for v in value:
                if (v[1] == val):
                    return v[0]
