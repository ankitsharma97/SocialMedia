from django.urls import path
from main.views import (
    HomeView, SearchView, LikePostView, FollowUserView,UnfollowUserView, FollowersView, AllPostView, FollowingView,
    AddPostView,UpdatePostView,delete_post, UpdateProfileView, ProfileView, AboutView, ContactView, LoginView, SignupView, LogoutView
)
from socialMedia import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('update_post/<int:id>', UpdatePostView.as_view() ,name='update_post'),
    path('delete_post/<int:id>', delete_post ,name='delete_post'),
    path('followers/<int:user_id>', FollowersView.as_view(), name='followers'),
    path('allpost/<int:user_id>', AllPostView.as_view(), name='allpost'),
    path('following/<int:user_id>', FollowingView.as_view(), name='following'),
    path('add_post', AddPostView.as_view(), name='add_post'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
