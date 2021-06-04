from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, BasePermission
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
	return HttpResponse('''
	<div style='text-align: center'>
	<h1>Django Blog API</h1>
	<p><a href=''>Click here</a> to get info about the API endpoints</p>
	<p>Blog API <a href=''>GitHub Repo</a></p>
	<p>Go to 'Future Diary' <a href=''>React App</a> (built on this API)</p>
	<p>React App <a href=''>GitHub Repo</a></p>
	</div>
	''')

def RedirectHome(request):
	return redirect('api/')

class IsAuthorOrReadOnly(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class BlogPostList(generics.ListCreateAPIView):
	queryset = BlogPost.objects.all().order_by('-date_published')
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = BlogPostSerializer
	lookup_field = 'slug'

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = BlogPost.objects.all()
	permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
	serializer_class = BlogPostSerializer
	lookup_field = 'slug'
