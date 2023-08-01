from django.shortcuts import render,redirect

from .serializers import (UserRegisterSerializer,
                          AdminRegisterSerializer,
                          BlogPostSerializer,
                          CommentSerializer,
                          AdminBlogPostSerializer)

from .models import (User,
                    BlogPost,
                    Comment)


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import generics,serializers
from rest_framework.generics import  RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from django.core.mail import send_mail
from django.conf import settings
from blogging_platform.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 

from .pagination import NumberPagination




#.........................................................USER SECTION.........................................................#



#..........................USER REGISTRATION AND MAIL SENDING..................................#

class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save() 
            
            subject = 'User Registration'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [account.email]

            html_content = render_to_string('email.html', {'username': account.username})
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

            data['response'] = 'message:User created'
            refresh = RefreshToken.for_user(account)
        else:
            data = serializer.errors
        return Response(data)



#..........................BLOGPOST CREATE..................................#

class BlogCreateView(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        blog_post = serializer.save(author=self.request.user)

        subject = 'Blog Post Creation'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]

        context = {
            'title': blog_post.blog_title,
            'content': blog_post.blog_content,
        }
        
        html_content = render_to_string('blogcreate.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")

        if blog_post.image:
            email.attach(blog_post.image.name, blog_post.image.read())

        email.send()


#..........................LIST ALL BLOGPOST..................................#

class BlogListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = NumberPagination

#..........................BLOGPOST RETRIEVE, UPDATE AND DELETE ..................................#


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Blog deleted successfully."})
        except NotFound:
            return Response({"message": "Blog not found."})  


#..........................COMMENT CREATE..................................#

class CommentCreateView(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        blog_post_id = self.kwargs['blog_post_id']  
        serializer.save(user=self.request.user, blog_post_id=blog_post_id)


#..........................VIEW ALL COMMENTS..................................#

class CommentListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = NumberPagination


    def get_queryset(self):
        blog_post_id = self.kwargs['blog_post_id']
        return Comment.objects.filter(blog_post_id=blog_post_id)


#..........................EDIT OR DELETE COMMENTS..................................#

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
            instance = self.get_object()
            if instance.user != self.request.user:
                raise PermissionDenied("You do not have permission to edit this comment.")
            return self.update(request, *args, **kwargs) 

    def delete(self, request, *args, **kwargs): 
            instance = self.get_object()
            if instance.user != self.request.user:
                raise PermissionDenied("You do not have permission to delete this comment.")
            self.perform_destroy(instance) 
            return Response({"message": "Comment deleted successfully."})




#.........................................................ADMIN SECTION.........................................................#


#..........................NEW ADMINUSER REGISTRATION..................................#

class AdminRegisterView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    def post(self, request, format=None):
        serializer = AdminRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'message:New Admin User created'
            refresh = RefreshToken.for_user(account)
        else:
            data = serializer.errors
        return Response(data)

#..........................ADMIN VIEW ALL BLOGS..................................#

class AdminBlogListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = BlogPost.objects.all()
    serializer_class = AdminBlogPostSerializer
    pagination_class = NumberPagination


#..........................ADMIN DELETE BLOGS..................................#


class AdminBlogDetailView(generics.DestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = BlogPost.objects.all()
    serializer_class = AdminBlogPostSerializer


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Blog deleted successfully."})
        except NotFound:
            return Response({"message": "Blog not found."})  

#..........................ADMIN VIEW ALL COMMENTS..................................#

class AdminCommentView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = NumberPagination


#..........................ADMIN DELETE BLOGS..................................#


class AdminCommentDetailView(generics.DestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Comment deleted successfully."})
        except NotFound:
            return Response({"message": "Comment not found."})  
