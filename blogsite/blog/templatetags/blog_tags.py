from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library() # used to register your own template tags and filters.

# simple template tag that returns the number of posts published so far
@register.simple_tag
def total_posts():
    return Post.published.count()


#inclusion tag  you can render a template with context variables returned by your template tag.
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    } # Inclusion tags have to return a dictionary of values, which is used as the context to render the specified template


#Tag to display the most commented post
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# register template filter
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

