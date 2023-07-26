from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import BlogPost,Comment

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email","first_name","last_name", "password", "password2"]

    def save(self):
        reg = User(
            username =self.validated_data['username'],
            email = self.validated_data['email'],
            first_name =self.validated_data['first_name'],
            last_name =self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password should match'})
        reg.set_password(password)
        reg.save()
        return reg


class AdminRegisterSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=True, write_only=True)  
    is_staff = serializers.BooleanField(default=True, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)


    class Meta:
        model = User
        fields = fields = ["id", "username", "email","password", "password2" ,"is_superuser", "is_staff"]

    def save(self):
        reg = User(
            username =self.validated_data['username'],
            email = self.validated_data['email'],
            is_superuser = self.validated_data['is_superuser'],
            is_staff = self.validated_data['is_staff'],

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
    
        if password != password2:
            raise serializers.ValidationError({'password': 'Password should match'})
        reg.set_password(password)
        reg.save()
        return reg



class CommentSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog_comment', 'created_time', 'updated_time']

    

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = BlogPost
        fields = ['id','author','blog_title','blog_content','created_time','updated_time','image','comments']



class AdminBlogPostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = ['id','author','blog_title','blog_content','created_time','updated_time','image']

