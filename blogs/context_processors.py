from .models import Category, Profile
from about.models import SocialLinks

def get_categories(request):
    categories = Category.objects.all()

    return dict (categories=categories)

def get_SocialLinks(request):
    social_links = SocialLinks.objects.all()
    return dict(social_links = social_links)

def get_profile(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
    return dict(profile=profile)