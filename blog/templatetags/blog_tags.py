from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()


# Custom template tag to display the total number of posts using simple_tag
@register.simple_tag
def total_posts():
    return Post.published.count()


# Custom template tag to display the latest posts using inclusion_tag
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# Custom template tag to display the most commented posts using inclusion_tag
@register.simple_tag
def get_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(
        total_comments=Count("comments")
    ).order_by("-total_comments")[:count]
    return most_commented_posts

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))