from django.db import models

# Create your models here.
class About(models.Model):
    about_heading = models.CharField(max_length=55)
    about_description = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return self.about_heading