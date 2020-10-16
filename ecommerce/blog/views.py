from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Post, Document
# it is used to protect a user from visiting a webpage without login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views.generic.edit import FormView 
# from .forms import GeeksForm 

# Create your views here.
# @login_required
# def home(request):
#  posts=Post.objects.all()
#  context={'posts':posts}
#  return render(request,'blog/home.html',context)

class PostListView(ListView):
 model=Post
 template_name='blog/home.html'
 context_object_name = 'posts'
 ordering = ['-date_posted']
 paginate_by = 6
 def post(self, request):
   search= self.request.POST.get('search')
   print(search)
   posts=Post.objects.filter(content__icontains=search).order_by('-date_posted')
   context={'posts':posts}
   return  render(request,'blog/home.html',context)

class UserPostListView(ListView):
 model=Post
 template_name='blog/user_posts.html'
 context_object_name = 'posts'
 
 paginate_by = 6

 def get_queryset(self):
  user=get_object_or_404(User, username=self.kwargs.get('username'))
  return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
 model=Post

class PostCreateView(LoginRequiredMixin, CreateView):
 model=Post
#  form_class = GeeksForm 
 fields = ['title', 'content', 'tag', 'category' ]

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)

 


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
 model=Post
 fields = ['title', 'content', 'tag', 'category']

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)
 
 def test_func(self):
  post = self.get_object()
  if self.request.user==post.author:
   return True
  return False
 
class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin,):
 model=Post
 success_url = '/blog/'
 def test_func(self):
  post = self.get_object()
  if self.request.user==post.author:
   return True
  return False
 
 
 

def knowledge(request):
#  group=request.user.groups
 publications=Document.objects.all()
 
 if request.method == 'POST':
   latest=request.POST.get('latest')
   search=request.POST.get('search')
   if latest:
    publications=Document.objects.all().order_by('-uploaded_at')
   if search:
    publications=Document.objects.filter(description__icontains=search)
 total_publication=publications.count()
 context={'publications':publications, 'total_publications':total_publication}

 return render(request,'blog/knowledge.html',context)

