'''
Created on Jan 31, 2017
Generate django views

@author: Zhongchao
'''

# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin, FormView
from django.views.generic.base import TemplateView
from models import *
from forms import *
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from .myChoices import *
from topics import *
from pdfhandler import *
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponseRedirect
from search import search_posts
from sortbynumber import sort_post
from numpy.ma.core import ids
import json
from createJson import *
from loadmodel import init
from createPost import create_new_post
import loadmodel

searchresult = ''

class TagListView(ListView):
    model = Tag
    context_object_name = "tag_list"

    def get_template_names(self):
        return ["blog/tag_list.html"]

    def get_queryset(self):
        return Tag.objects

'''
    generate list view for posts with pagination effect
'''
class PostListView(ListView):
    model = Post
    context_object_name = "post_list"
    paginate_by = 10
    
    def get_template_names(self):
        return ["blog/post_list.html"]
    
    def get_queryset(self):
        #posts = Post.objects
        posts = sort_post()
        #posts = posts.filter(is_published=True).order_by('-maxnumber')
        return posts
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs) 
        #list_post = Post.objects.all()
        list_post = self.get_queryset()
        paginator = Paginator(list_post, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_post = paginator.page(page)
        except PageNotAnInteger:
            file_post = paginator.page(1)
        except EmptyPage:
            file_post = paginator.page(paginator.num_pages)

        context['post_list'] = file_post
        return context


'''
    generate search keyword view
'''   
class PostSearchView(FormMixin, ListView):
    model = Post
    form_class = SearchForm
    context_object_name = "post_search"
    paginate_by = 10

    def get_template_names(self):
        return ["blog/post_search.html"]
    
    def get_success_url(self):
        return reverse('post-search')
    
    def get_queryset(self):
        global searchresult
        if 'search' in self.request.GET:
            searchresult = self.request.GET['title']

        posts = search_posts(searchresult)
        return posts

    def get_context_data(self, **kwargs):
        context = super(PostSearchView, self).get_context_data(**kwargs) 
        list_post = self.get_queryset()
        paginator = Paginator(list_post, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_post = paginator.page(page)
        except PageNotAnInteger:
            file_post = paginator.page(1)
        except EmptyPage:
            file_post = paginator.page(paginator.num_pages)

        context['post_search'] = file_post
        return context    

'''
    generate view for creating new post
'''    
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_template_names(self):
        return ["blog/post_create.html"]

    def get_success_url(self):
        return reverse('post-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        try:
            http = super(PostCreateView, self).form_valid(form)
            messages.success(self.request, "Post created.")
            return http
        except:
            messages.success(self.request, "Duplicated title.")
            return HttpResponseRedirect('/')


'''
    generate view for reading post detail
'''   
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

    def get_template_names(self):
        return ["blog/post_detail.html"]

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]    


'''
    generate view for updating existing post
'''
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    context_object_name = "post"

    def get_template_names(self):
        return ["blog/post_update.html"]

    def get_success_url(self):
        return reverse('post-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            http = super(PostUpdateView, self).form_valid(form)
            messages.success(self.request, "Post updated.")
            return http
        except:
            messages.success(self.request, "Duplicated title.")
            return HttpResponseRedirect('/')

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]


'''
    generate view for deleting existing post
'''
class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post-list')   
    
    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Post removed.")
        return redirect(self.get_success_url())        

    def get_object(self):
        return Post.objects(id=self.kwargs['pk'])[0]


'''
    generate view for adding new topics
'''
class AddTopicView(FormView):
    model = TopicList
    form_class = AddTopicsForm
    context_object_name = "handle-topic"

    def get_template_names(self):
        return ["blog/add_topic.html"]
    
    def get_success_url(self):
        return reverse('add-topics')
    
    def form_valid(self, form):
        request_topic(self.request)
        return super(AddTopicView, self).form_valid(form)


'''
    generate view for narrowing down topics
''' 
class SelectTopicView(FormView):
    form_class = SelectTopicsForm
    context_object_name = "select-topics"

    def get_template_names(self):
        return ["blog/select_topic.html"]
    
    def get_success_url(self):
        return reverse('select-topics')
    
    def form_valid(self, form):
        save_choices(self.request)
        return super(SelectTopicView, self).form_valid(form)


'''
    generate view for researcher profile
'''
class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    context_object_name = "profile"
    
    def get_template_names(self):
        return ["blog/researcher-profile.html"]
    
    def get_success_url(self):
        return reverse('researcher-profile', kwargs={'pk': self.object.id})
   
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file') # files are the handlers for multiple uploaded files
        ids = []
        if form.is_valid():
            if (self.request.POST.get('save') == 'save'):
                loadmodel.init()
                for f in files:
                    title, abstract = handle_uploaded_file(f)  # Do something with each file.
                    post_id = create_new_post(title, abstract)
                    ids.append(post_id)
                self.object = form.save(ids, commit=True)
            elif (self.request.POST.get('load') == 'load'):
                self.get_object()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
       
    def get_object(self):
        try:
            return Profile.objects(author=self.request.POST.get('author'))[0]
        except:
            if 'pk' in self.kwargs:
                return Profile.objects(id=self.kwargs['pk'])[0] 
            else:
                return None
    

'''
    generate view for loading pdf files
'''    
class LoadfileView(FormView):
    model = File
    form_class = UploadFileForm
    context_object_name = "load-file"

    def get_template_names(self):
        return ["blog/load_file.html"]
    
    def get_success_url(self):
        return reverse('load-file')
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        ids = []
        if form.is_valid():
            for f in files:
                title, abstract = handle_uploaded_file(f)  # Do something with each file.
                post_id = create_new_post(title, abstract)
                ids.append(post_id)
            self.object = form.save(ids, commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


'''
    processing the request for uploading pdf files
'''
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        title, abstract = handle_uploaded_file(request.FILES['file'])
        messages.success(request, "File uploaded.")
        create_new_post(title, abstract)


'''
    processing the request for adding or resetting research topics
'''   
@csrf_exempt    
def request_topic(request):
    if (request.POST.get('addtopic') == 'add'):
        try:
            addtopic(request.POST.get('category'), request.POST.get('topic'), request.POST.get('value'))
            messages.success(request, "Topic Added.")
        except:
            messages.success(request, "Duplicated topic.")
    elif (request.POST.get('reset') == 'reset'):
        resettopic()
        messages.success(request, "Topic Reset.")


'''
    processing the request for getting topics for a particular category
'''             
@csrf_exempt
def get_topics(request, pk):
    #dropdown_id = request.POST['dropdown_id']
    #topics = TopicList.objects.filter(category=dropdown_id).order_by('value')
    topics = TopicList.objects.filter(category=pk).order_by('value')
    topic_dict = []
    topic_dict.append({'None':"-----"})
    for topic in topics:
        topic_dict.append({topic.value:topic.value})
    response = { 'item_list':topic_dict }

    return HttpResponse(simplejson.dumps(response), mimetype="application/json")


'''
@csrf_exempt
def get_choices(request, pk):
    #categories_id = request.POST['categories_id']
    #topics = TopicList.objects.filter(category=categories_id).order_by('value')
    topics = TopicList.objects.filter(category=pk).order_by('value')
    topic_dict = []
    for topic in topics:
        topic_dict.append({topic.value:topic.value})
    response = { 'item_list':topic_dict }

    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
       
         
@csrf_exempt
def get_profilechoices(request, pk):
    #cats_id = request.POST['cats_id']
    #topics = TopicList.objects.filter(category=cats_id).order_by('value')
    topics = TopicList.objects.filter(category=pk).order_by('value')
    topic_dict = []
    for topic in topics:
        topic_dict.append({topic.value:topic.value})
    response = { 'item_list':topic_dict }

    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
'''

'''
    processing the request for getting article content for a particular article title
'''  
@csrf_exempt
def get_abstract(request, pk):
    titles_id = request.POST['titles_id']
    post = Post.objects.filter(title__icontains = titles_id).first()
    topic_dict = []
    if post:
        topic_dict.append({post.text:post.tags})

    response = { 'item_list':topic_dict }

    return HttpResponse(simplejson.dumps(response), mimetype="application/json")


'''
    processing the request for getting json data for a particular author and a list of topics
'''
@csrf_exempt
def get_image(request, author, filter):
    print author, filter
    filter = filter.split('urls=')
    filter = [f.strip('&') for f in filter]
    if (len(filter) > 1 and filter[0] == ''):
        filter = filter[1:]
    response = create_json(author, filter)
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")


'''
    processing the request for getting titles for a particular author and a list of topics
'''  
@csrf_exempt
def get_title(request, pk):
    author_id = request.POST['author_id']
    filter_id = request.POST['filter_id']
    ids = Profile.objects.filter(author__exact = author_id).first().ids
    topic_dict = []
    topic_dict.append({'-----':"-----"})
    for id in ids:
        post = Post.objects.get(pk = id)
        if (filter_id == "" or filter_id in post.tags):
            topic_dict.append({post.title:post.title})

    response = { 'item_list':topic_dict }

    return HttpResponse(simplejson.dumps(response), mimetype="application/json")


'''
    processing the request for narrowing down research topics
'''  
def save_choices(request):
    if (request.POST.get('select') == 'select'):
        categories = request.POST.get('categories')
        topics = list(request.POST.getlist('topics'))
        selecttopic(categories, topics)
        messages.success(request, "Topic Selected.")  
        
           