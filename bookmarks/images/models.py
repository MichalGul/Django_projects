from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
# This is the model that you will use to store images retrieved from different sites
class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)  # image is deleted when user is deleted
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)

    # many to many relation, django automatically creates intermediary join table, can be defined in Images or in users
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank = True)

def __str__(self):
    return self.title


# Override the save() method of the Image model to automatically generate the slug field based on the value of the title field
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
