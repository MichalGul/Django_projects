from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from blogsite.settings import EMAIL_HOST_USER
from taggit.models import Tag
from django.db.models import Count # This is the Count aggregation function of the Django ORM. This function will allow you to perform aggregated counts of tags. django.db.models includes the following aggregation functions:


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET: # send the form using the GET method instead of POST
        form = SearchForm(request.GET) #When the form is submitted, you instantiate it with the submitted GET data, and verify that the form data is valid
        if form.is_valid():
            query = form.cleaned_data['query']
            #create a SearchQuery object, filter results by it, and use SearchRank to order the results by relevancy.
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)

            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query':query,
                   'results':results}
                  )

# Class based view see urls.py in blog app to usage
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Regular mangual view
def post_list(request, tag_slug=None):  # parametr reqeust jest wymagany przez wszystkie funkcjie widoków
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)  # 3 post in each page
    print(request.GET)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)

    return render(request=request, template_name='blog/post/list.html',
                  context={'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts using model agregatuin functions
    post_tags_ids = post.tags.values_list('id', flat=True) # retrieve list of ids of the tags of current post values_list() QuerySet returns tuples with the values for the given fields. You pass flat=True to it to get single values such as [1, 2, 3, ...] instead of one-tuples such as [(1,), (2,), (3,) ...].
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) # Get all posts that contain any of these tags excluding current post
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] # You use the Count aggregation function to generate a calculated field—same_tags—that contains the number of tags shared with all the tags queried.
    # then You order the result by the number of shared tags (descending order) and by publish to display recent posts first for the posts with the same number of shared tags. You slice the result to retrieve only the first four posts.


    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submited
        form = EmailPostForm(request.POST)  # from filled with user data
        if form.is_valid():
            # Form fields passes validation
            cd = form.cleaned_data  # If your form data does not validate, cleaned_data will contain only the valid
            # fields.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomends your read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']} 's comments: {cd['comments']}"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()  # empty form
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
