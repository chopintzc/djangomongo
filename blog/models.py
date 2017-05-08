'''
Created on Jan 22, 2017
Generate post models

@author: Zhongchao
'''

from datetime import datetime
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse
from .myChoices import *

'''
	model for topic
'''
class Tag(Document):
	title = StringField(max_length=200, required=True)
	
	def __unicode__(self):
		return self.title

'''
	model for category
'''
class Dropdown(Document):
	# category name
	title = StringField(max_length=200, required=True)
    
	def __unicode__(self):
		return self.title


'''
	model for topic
'''       
class MyTopics(Document):
	# topic name
	title = StringField(max_length=200, required=True)
	
	# topic NSERC ID number
	value = StringField(max_length=200, required=True)
	
	def __unicode__(self):
		return self.title


'''
	model for list of topics
'''
class TopicList(Document):
	category = StringField(max_length=200, required=True) 
	topic = StringField(max_length=200, required=True, unique=True)
	value = StringField(max_length=200, required=True, unique=True)
	
	def __unicode__(self):
		return self.topic


'''
	model for pdf file
'''
class File(Document):
    file = FileField()


'''
	model for researcher profile
'''    
class Profile(Document):
	# researcher name
	author = StringField(max_length=200, required=True, unique=True)
	
	# research topics
	tags = ListField(StringField(max_length=200, required=False))
	
	# ids for all the articles saved in the MongoDB database
	ids = ListField(ObjectIdField(required=False))
	
	def __unicode__(self):
		return self.author
	
'''
	model for each research article
'''	
class Post(Document):
	# it's not used any more
	user = ReferenceField(User, reverse_delete_rule=CASCADE)
	
	# article title
	title = StringField(max_length=200, required=True, unique=True)
	
	# article abstract/content
	text = StringField(required=True)
	
	# it's not used any more
	text_length = IntField()
	
	# it's not used any more
	date_modified = DateTimeField(default=datetime.now)
	
	# it's not used any more
	is_published = BooleanField()
	
	# research topics
	tags = ListField(StringField(max_length=200, required=False))
	
	# it's not used any more
	maxnumber = IntField()
    
	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.text_length = len(self.text)
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post-detail', args=[self.id])

	def get_edit_url(self):
		return reverse('post-update', args=[self.id])

	def get_delete_url(self):
		return reverse('post-delete', args=[self.id])		
	
