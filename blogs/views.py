from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import F
from .models import Blog , Category, Comment
from django.db.models import Q

# Create your views here.

def posts_by_category(request, category_id):

    posts_qs = Blog.objects.filter(category = category_id, status='Published').order_by('-created_at')
    page_number = request.GET.get('page')
    paginator = Paginator(posts_qs, 5)
    posts = paginator.get_page(page_number)

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



def blogs(request, slug):
    post = get_object_or_404(Blog,slug=slug,status='Published')

    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = post
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)

    # Count the view once per session to avoid duplicate increments on refresh.
    session_key = f'viewed_blog_{post.pk}'
    if not request.session.get(session_key, False):
        Blog.objects.filter(pk=post.pk).update(views=F('views') + 1)
        request.session[session_key] = True
        post.refresh_from_db()

    #Comments:
    comments = Comment.objects.filter(blog = post)
    comments_count = comments.count()

    related_posts = Blog.objects.filter(
        category=post.category,
        status='Published'
    ).exclude(pk=post.pk).order_by('-created_at')[:3]

    context = {
        'post': post,
        'comments': comments,
        'comments_count' : comments_count,
        'related_posts': related_posts,
    }

    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    page_number = request.GET.get('page')

    blogs_qs = Blog.objects.filter(
        Q(title__icontains = keyword) | Q(short_description__icontains = keyword) | Q(blog_body__icontains = keyword), status = 'Published'
        ).order_by('-created_at')

    paginator = Paginator(blogs_qs, 5)
    blogs = paginator.get_page(page_number)

    context = {
        'blogs' : blogs,
        'keyword' : keyword,
    }
    return render(request, 'search.html', context)