from django.shortcuts import render, redirect
from django.http import HttpResponse
from blogs.models import Category, Blog
from about.models import About
from .forms import RegistrationForm


def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured = True, status = 'Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured = False, status = 'Published')
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
            form.save()
            return redirect('register')
        else:
            return(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'register.html', context)