from django.shortcuts import render, redirect
from django.http import HttpResponse
from blogs.models import Category, Blog, Profile
from about.models import About
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme




def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured = True, status = 'Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured = False, status = 'Published').order_by('-created_at')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'featured_posts' : featured_posts,
        'posts' : posts,
        'about' : about
    }
    return render(request, 'home.html', context )

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            return redirect('login')
        else:
            return(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'register.html', context)


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit_profile.html', context)


def login(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = None

    if request.method =='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(next_url or 'dashboard')
    else:
        form= AuthenticationForm()
    context = {
        'form': form,
        'next': next_url,
    }

    return render(request,'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')
