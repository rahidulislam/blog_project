from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from .forms import EmailPostForm


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts})


class PostListView(ListView):
    """Alternative to post_list view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, slug):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Post does not exist")
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/post/detail.html", {"post": post})


# post share
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cd["to"]])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})
