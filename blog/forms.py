'''
Created on Feb 21, 2017
Generate app forms

@author: Zhongchao
'''

#from bson import ObjectId
from bson.objectid import ObjectId
from django import forms
from models import *
from .myChoices import *
from django.core.exceptions import ValidationError
import ast
import re
import operator

'''
    create customized MultipleChoiceField without choicefield validation
'''
class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass
    
def validate_all_choices(value):
    # here have your custom logic
    pass

'''
    find out topics for a couple of post ids
'''
def extract_tags(ids):
    groups = {}
    tags = []
    for id in ids:
        tag = Post.objects.get(pk = id).tags
        for t in tag:
            if t not in groups:
                groups[t] = 1
            else:
                groups[t] = groups[t] + 1
    while any(groups):
        t = max(groups.iteritems(), key=operator.itemgetter(1))[0]
        tags.append(t)
        del groups[t]
    return tags
    
'''
    find out titles for a couple of post ids
'''
def extract_titles(ids):
    titles = []
    titles.append('-----')
    for id in ids:
        title = Post.objects.get(pk = id).title
        titles.append(title)
    return titles

'''
    Form for narrow down research topics
'''        
class SelectTopicsForm(forms.Form):
    categories = forms.ChoiceField(
        choices=Category,
        required=False,
        validators=[validate_all_choices])
    
    topics = forms.CharField(
        widget=forms.SelectMultiple(),
        required=False)
    
    
'''
    Form for generating researcher profile
'''  
class ProfileForm(forms.Form):    
    # research topics
    tags = MultipleChoiceFieldNoValidation(widget=forms.widgets.CheckboxSelectMultiple(), required=False)
    
    # ids for all the literatures in the MongoDB database
    ids = forms.CharField(required=False)
    
    # cats = forms.ChoiceField(choices=Category, required=False, validators=[validate_all_choices])
    
    # tps is not actually used as more
    tps = forms.CharField(widget=forms.SelectMultiple(), required=False)
        
    # research name
    author = forms.CharField(max_length=255, required=True)
    
    # literature title
    titles = forms.ChoiceField(required=False)
    
    # literature abstract
    abstract = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols': 90, 'rows': 10}), required=False)
    
    # literature topics
    tp = forms.CharField(widget=forms.SelectMultiple(), required=False)
    
    # pdf files
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    # filt = forms.CharField(max_length=255, required=False)
    
    # create a blank form for Create view or load in a filled form for Update view
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['author'].initial = self.instance.author
            return_tags = extract_tags(self.instance.ids)
            self.fields['tags'].choices = [(tag, tag) for tag in return_tags]
            self.fields['tags'].initial = [tag for tag in return_tags]
            self.fields['ids'].initial = self.instance.ids
            self.fields['titles'].choices = [(tag, tag) for tag in extract_titles(self.instance.ids)]
            self.fields['titles'].initial = [tag for tag in extract_titles(self.instance.ids)]
            
    # save cleaned data to profile model      
    def save(self, ids, commit=True):
        profile = self.instance if self.instance else Profile()
        profile.author = self.cleaned_data['author']
        profile.tags = [tag for tag in self.cleaned_data['tags']]
        profile.ids = ids
        
        # this condition is not used anymore
        if str(self.cleaned_data['tps']) != 'None' and str(self.cleaned_data['tps']) != '':
            tmp = [item.encode('ascii') for item in ast.literal_eval(self.cleaned_data['tps'])]
            for t in tmp:
                profile.tags.append(t)            
        if commit:
            profile.save()
                
        return profile    


'''
    Form for uploading pdf files
''' 
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    author = forms.CharField(max_length=255, required=True)
    
    def save(self, ids, commit=True):
        profile = Profile()
        profile.author = self.cleaned_data['author']
        profile.ids = ids
          
        if commit:
            profile.save()
                
        return profile
    

'''
    Form for creating or updating post
'''    
class PostForm(forms.Form):
    # title of article
    title = forms.CharField(max_length=255)
    
    # content/abstract of article
    text = forms.CharField(widget=forms.widgets.Textarea())
    
    # it's not used any more
    is_published = forms.BooleanField(required=False)
    
    # research topics
    tags = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple(), required=False)
    
    # drop down menu for the research category 
    dropdown = forms.ChoiceField(choices=Category, required=False, validators=[validate_all_choices])
    
    # drop down menu for the research topics 
    mytopics = forms.CharField(widget=forms.Select(), required=False)
    
    # create a blank form for Create view or load in a filled form for Update view
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(PostForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['text'].initial = self.instance.text
            self.fields['is_published'].initial = self.instance.is_published    
            self.fields['tags'].choices = [(tag, tag) for tag in self.instance.tags]
            self.fields['tags'].initial = [tag for tag in self.instance.tags]
    
    # save cleaned data to post model 
    def save(self, commit=True):
        post = self.instance if self.instance else Post()
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.is_published = self.cleaned_data['is_published']
        post.tags = [tag for tag in self.cleaned_data['tags']]
        
        # append selected topic to the tags
        if str(self.cleaned_data['mytopics']) != 'None' and str(self.cleaned_data['mytopics']) != '':
            post.tags.append(self.cleaned_data['mytopics'])
        if commit:
            post.save()
                
        return post


'''
    Form for searching posts
'''
class SearchForm(forms.Form):
    # keyword in the article title
    title = forms.CharField(max_length=255)


'''
    Form for adding research topics
'''
class AddTopicsForm(forms.Form):
    category = forms.ChoiceField(
        choices=Category,
        required=False,
        validators=[validate_all_choices])
    topic = forms.CharField(max_length=255, required=False,)
    value = forms.CharField(max_length=255, required=False,)

    
