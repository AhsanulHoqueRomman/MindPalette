from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog , Category

# Create your views here.

def posts_by_category(request, category_id):

    posts = Blog.objects.filter(category = category_id, status='Published')
    category = Category.objects.get(pk = category_id )
    context = {
        'posts' : posts,
        'category' :  category
    }

    return render(request, 'posts_by_category.html', context)