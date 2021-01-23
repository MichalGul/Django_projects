from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from blogsite.settings import EMAIL_HOST_USER


# Class based view see urls.py in blog app to usage
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Create your views here.
def post_list(request):  # parametr reqeust jest wymagany przez wszystkie funkcjie widoków
    posts = Post.published.all()
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

    return render(request=request, template_name='blog/post/list.html', context={'posts': posts, 'page': page})


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
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


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
