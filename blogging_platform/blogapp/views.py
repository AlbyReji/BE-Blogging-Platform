from django.shortcuts import render,redirect

from .serializers import (UserRegisterSerializer,
                          AdminRegisterSerializer,
                          BlogPostSerializer,
                          CommentSerializer)

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



#.........................................................USER SECTION.........................................................#



#..........................USER REGISTRATION AND MAIL SENDING..................................#

class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            send_mail(
                subject= 'user Registration',
                message= 'Account is created ,Please login',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list= [account.email] 
                )    
                
            data['response'] = 'message:User created'
            refresh = RefreshToken.for_user(account)
        else:
            data = serializer.errors
        return Response(data)


#..........................LIST ALL BLOGPOST..................................#

class BlogListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


#..........................BLOGPOST CREATE..................................#

class BlogCreateView(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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
