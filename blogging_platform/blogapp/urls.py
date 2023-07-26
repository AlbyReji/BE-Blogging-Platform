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
    path('commentlist/<int:blog_post_id>/', views.CommentListView.as_view(), name='list_comments_by_blog_post'),
    path('commentdetail/<int:pk>/',views.CommentDetailView.as_view(),name = "commentdetail"),


    path('adminregister/',views.AdminRegisterView.as_view(),name = "adminregister"),
    path('adminlist/',views.AdminBlogListView.as_view(),name = "adminlist"),
    path('admindetail/<int:pk>/',views.AdminBlogDetailView.as_view(),name = "admindetail"),
    path('admin_commentlist/',views.AdminCommentView.as_view(),name = "admin_commentlist"),
    path('admin_commentdetail/<int:pk>/',views.AdminCommentDetailView.as_view(),name = "admindetail"),



]