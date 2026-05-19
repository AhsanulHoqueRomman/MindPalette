from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse
from .models import Blog , Category

# Create your views here.

def posts_by_category(request, category_id):

    posts = Blog.objects.filter(category = category_id, status='Published')
    # Use try/except block when we want to do some custom action if the category does not exist.
    # try:
    #     category = Category.objects.get(pk = category_id )
    # except:
    #     #redirect the user to home.
    #     return redirect('home')
    
    #Use get_object_or_404 when we want to show 404 error page if the category doesn't exist.
    category = get_object_or_404(Category, pk = category_id)

    context = {
        'posts' : posts,
        'category' :  category
    }

    return render(request, 'posts_by_category.html', context)