from django.contrib import admin
from .models import About, SocialLinks

# Register your models here.

class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):              #This Function is used for limiting to add about not more than 1 in django admin.
        count = About.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(About, AboutAdmin)
admin.site.register(SocialLinks)