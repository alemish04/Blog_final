from django.urls import path
from django.contrib import admin
from . import views
from .views import *

urlpatterns = [
    # path('', Bloglist.as_view(), name='home'),
    # path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    # path('about/', AboutPageView.as_view(), name='about'),
    #
    # path('s/', SearchResultView.as_view(), name="search_result_url")
    path("", post_list, name="posts_list_url"),
    path('admin/', admin.site.urls, name="admin"),
    path("post/<int:id>/", post_detail, name="post_detail_url"),
    path("categories/", category_list, name="category_list_url"),
    path("category/<int:id>/", category_detail, name="category_detail_url"),
    path("about/", about_project, name="about_project_url"),
    path('login', views.MyprojectLoginView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.MyProjectLogout.as_view(), name='logout_page'),
    # path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    # path('create_profile_page/', CreateProfilePageView.as_view(), name='create_user_profile'),
    # path('edit_profile_page/', EditProfilePageView.as_view(), name="edit_user_profile")
    path('profile/<username>/', profile, name='profile'),
    # path('edit-profile/', edit_profile, name='edit_profile'),
]
