from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, BasePermission

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
