from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, ListView,UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Post, UserProfile, Follow
from .forms import LoginForm as AuthenticationForm, SignUpForm, PostForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User





class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        print(user)
        follow_user = Follow.objects.filter(follower=user)
        followed_user = Follow.objects.filter(followed_user=user)
        user_profile = UserProfile.objects.get(username=user.username)
        print(user_profile)
        posts = Post.objects.filter(username=user.username)
        is_following = False
                
        if request.user.is_authenticated:
            print(user)
            is_following = Follow.objects.filter(followed_user=user, follower=request.user).exists()

        print(is_following)
        return render(request, 'profile.html', {
            'user_profile': user_profile,
            'posts': posts,
            'follow_user': follow_user,
            'followed_user': followed_user,
            'is_following': is_following,
            'user_id': user.id, 
        })


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date') 
        follows = Follow.objects.filter(follower=request.user) if request.user.is_authenticated else None

        posts_with_mappings = []
        for post in posts:
            user_profile = UserProfile.objects.get(username= post.username)
            follow_mapping = follows.filter(followed_user__username=post.username).exists() if follows else False
            like_count = post.likes.count()
            is_liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            posts_with_mappings.append(
                {'post': post, 'follow_mapping': follow_mapping, 'like_count': like_count, 'is_liked': is_liked,'user_profile':user_profile})

        return render(request, 'home.html', {'posts_with_mappings': posts_with_mappings})


class SearchView(View):
    def get(self, request):
        username = request.GET.get('q')
        try:
            user = User.objects.get(username=username)
            return redirect('profile', username=user.username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('home')
        


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('home')


class FollowUserView(LoginRequiredMixin, View):
    def get(self, request, username):
        followed_user = User.objects.get(username=username)
        user = User.objects.get(username=username)
        if request.user != followed_user:
            Follow.objects.get_or_create(follower=request.user, followed_user=followed_user)
        return redirect('profile', username=user.username)


class UnfollowUserView(LoginRequiredMixin, View):
    def get(self, request, username):
        followed_user = User.objects.get(username=username)
        user = User.objects.get(username=username)
        Follow.objects.filter(follower=request.user, followed_user=followed_user).delete()
        return redirect('profile', username=user.username)


class FollowingView( ListView):
    model = Follow
    template_name = 'followers.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        profile = UserProfile.objects.get(pk=user_id)
        user = User.objects.get(username=profile.username)
        return Follow.objects.filter(follower=user)




class FollowersView(ListView):
    model = Follow
    template_name = 'following.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        profile = UserProfile.objects.get(pk=user_id)
        user = User.objects.get(username=profile.username)
        return Follow.objects.filter(followed_user=user)



class AllPostView(ListView):
    model = Post
    template_name = 'allpost.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        profile = UserProfile.objects.get(pk=user_id)
        user = User.objects.get(username=profile.username)
        return Post.objects.filter(username=user.username)
    


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class AddPostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'addpost.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            desc = form.cleaned_data['desc']
            img = form.cleaned_data['img']
            video = form.cleaned_data['video']
            username = request.user.username
            post = Post(desc=desc, username=username, img=img, video=video)
            post.save()
            return redirect('profile',user_id = request.user.id)
        return render(request, 'addpost.html', {'form': form})
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'updatepost.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        return Post.objects.get(pk=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return redirect('profile',username=request.user.username)
    else:
        return  redirect('login')
    


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        pi = UserProfile.objects.get(username=request.user.username)
        form = SignUpForm(instance=pi)
        return render(request, 'updateprofile.html', {'form': form})

    def post(self, request):
        pi = UserProfile.objects.get(username=request.user.username)
        form = SignUpForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
            return redirect('profile',user_id = request.user.id)
        return render(request, 'updateprofile.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'login.html', {'form': form})


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['Confirm_Password']
            profile_pic = form.cleaned_data['profile_pic']
            about = form.cleaned_data['about']
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'form': form, 'error': 'Username already taken'})
            if password != confirm_password:
                return render(request, 'signup.html', {'form': form, 'error': 'Passwords do not match'})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user_profile = UserProfile.objects.create(username=username, email=email, password=password, name=name, profile_pic=profile_pic, about=about)
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
        return render(request, 'signup.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('home')