from django.urls import path
from main.views import (
    HomeView, SearchView, LikePostView, FollowUserView,UnfollowUserView, FollowersView, AllPostView, FollowingView,
    AddPostView, UpdateProfileView, ProfileView, AboutView, ContactView, LoginView, SignupView, LogoutView
)
from socialMedia import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('follow/<int:post_id>/', FollowUserView.as_view(), name='follow_user'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('allpost/', AllPostView.as_view(), name='allpost'),
    path('following/', FollowingView.as_view(), name='following'),
    path('add_post', AddPostView.as_view(), name='add_post'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('unfollow/<int:post_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
