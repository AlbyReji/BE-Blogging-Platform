from django.urls import path
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name = "register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('bloglist/',views.BlogListView.as_view(),name = "bloglist"),
    path('bloglistcreate/',views.BlogCreateView.as_view(),name = "bloglistcreate"),
    path('blogdetail/<int:pk>/',views.BlogDetailView.as_view(),name = "blogdetail"),

    path('commentcreate/<int:blog_post_id>/',views.CommentCreateView.as_view(),name = "commentcreate"),

    path('adminregister/',views.AdminRegisterView.as_view(),name = "adminregister"),
]