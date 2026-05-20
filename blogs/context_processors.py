from .models import Category
from about.models import SocialLinks

def get_categories(request):
    categories = Category.objects.all()

    return dict (categories=categories)

def get_SocialLinks(request):
    social_links = SocialLinks.objects.all()
    return dict(social_links = social_links)