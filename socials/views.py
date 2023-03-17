from django.shortcuts import render
from socials.models import Profile, Posts, Comments
from django.contrib.auth.models import User
from socials.forms import UserForm, ProfileForm, LoginForm,PostsForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, UpdateView, ListView, CreateView, TemplateView 
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages


# Create your views here.
def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'You must login first')
            return redirect('signin')
        else:
            return fn(request, *args, **kwargs)
    return wrapper
decs=[signin_required,never_cache]

@signin_required
@never_cache
def sign_out_view(request, *args, **kwargs):
    logout(request)
    return redirect('signin')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            usr= authenticate(request, username=uname, password=pwd)
            if usr:
                login(request,usr)
                print(request.user)
                messages.success(request,'Login Success')
                return redirect('home')
                
            else:
                messages.error(request,'Invalid credentials')
                return redirect('signin')


class IndexView(ListView):
    template_name= 'index.html'
    model = Posts
    context_object_name = 'posts'
    def get_queryset(self):
        return Posts.objects.exclude(user=self.request.user.profile).order_by("-created_date")

# class ProfileView(ListView):
#     template_name='index.html'
#     model=Profile
#     context_object_name= 'profiles'
#     def get_queryset(self):
#         return Profile.objects.filter(user=self.request.user.profile)

def signup(request):
    if request.method == 'POST':
        #USER HAS INFO AND WANTS ACCOUNT___NOW!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =  User.objects.get(username=request.POST['username'])
                return render(request,'login.html',{'error':'Username Exist...Try Something Else !','username':user})
            except User.DoesNotExist :
                user = User.objects.create_user(username=request.POST['username'], password = request.POST['password1'],first_name=request.POST['firstname'],last_name=request.POST['lastname'],email=request.POST['email'],)
                profile = user.profile # because of signal and one2one relation
                profile.bio = request.POST['bio']
                profile.location = request.POST['location']
                profile.save()
                login(request,user)              
                return redirect('home')
        return render(request,'signin.html',{'error':"Passwords Don't Match"})
    else:
        return render(request,'signup.html')  

@signin_required
@never_cache
def update_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profile_pic
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_pic = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_pic = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()  
        
        return redirect('editprofile')
    return render(request, 'updateprofile.html', {'user_profile': user_profile})


decs
class AddPostView(CreateView):
    template_name="createpost.html"
    form_class = PostsForm
    success_url = reverse_lazy('home')
    model = Posts
    context_object_name = 'posts'

    def form_valid(self, form):
        form.instance.user=self.request.user.profile
        messages.success(self.request,'post added successfully')
        return super().form_valid(form)
 
    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user)

class MyProfileView(ListView):
    template_name='profile.html'
    success_url = reverse_lazy('profile')
    context_object_name = 'posts'

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user.profile)
    

@signin_required
@never_cache
def like_post(request,*args,**kwargs):
    id=kwargs.get('id')
    post=Posts.objects.get(id=id)
    usr=request.user.profile
    post.likes.add(usr)
    return redirect('home')

@signin_required
@never_cache
def add_cmnts(request,*args,**kwargs):
    id=kwargs.get('id')
    post=Posts.objects.get(id=id)
    cmt = request.POST.get('comment')
    Comments.objects.create(post=post,comment=cmt,user=request.user.profile)
    messages.success(request,"your comment is posted")
    return redirect('home')

@signin_required
@never_cache
def cmt_like(request,*args,**kwargs):
    id=kwargs.get('id')
    ans=Comments.objects.get(id=id)
    usr=request.user.profile
    ans.cmt_likes.add(usr)
    return redirect('home')

@signin_required
@never_cache
def deletepost(request,*args,**kwargs):
    id=kwargs.get('id')
    Posts.objects.get(id=id).delete()
    return redirect('profile')

@signin_required
@never_cache
def follow(request,*args,**kwargs):
    id=kwargs.get('id')
    profile=Profile.objects.get(id=id)
    usr=request.user
    profile.followers.add(usr)
    return redirect('home')
