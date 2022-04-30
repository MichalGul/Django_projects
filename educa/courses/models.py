from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, default="slug")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f'{self.order}. {self.title}'

class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     # generic relation to associate objects from different models that represent different types of content
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('text', 'video', "image", 'file')}) # limit the ConentType objects that can be used for the generic relation
    object_id = models.PositiveIntegerField()
    # Only the content_type and object_id fields have a corresponding column in the database table of this model.
    # The item field allows you to retrieve or set the related object directly, and its functionality is built on
    # top of the other two fields.
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related', # placeholder for child model class name
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string( #renders template with context as as string
            f'courses/content/{self._meta.model_name}.html', # used appropriate template for model (text, video, image or file)
            {'item': self}
        )

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.ImageField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
