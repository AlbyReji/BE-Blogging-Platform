from django.contrib import admin
from blogapp.models import User,BlogPost,Comment


admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Comment)
