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
	title = StringField(max_length=200, required=True)
    
	def __unicode__(self):
		return self.title


'''
	model for topic
'''       
class MyTopics(Document):
	title = StringField(max_length=200, required=True)
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
	author = StringField(max_length=200, required=True, unique=True)
	tags = ListField(StringField(max_length=200, required=False))
	ids = ListField(ObjectIdField(required=False))
	
	def __unicode__(self):
		return self.author
	
'''
	model for each research article
'''	
class Post(Document):
	user = ReferenceField(User, reverse_delete_rule=CASCADE)
	title = StringField(max_length=200, required=True, unique=True)
	text = StringField(required=True)
	text_length = IntField()
	date_modified = DateTimeField(default=datetime.now)
	is_published = BooleanField()
	tags = ListField(StringField(max_length=200, required=False))
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
	
