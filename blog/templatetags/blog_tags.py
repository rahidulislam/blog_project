from django import template
from ..models import Post
register = template.Library()

# Custom template tag to display the total number of posts using simple_tag
@register.simple_tag
def total_posts():
    return Post.published.count()

# Custom template tag to display the latest posts using inclusion_tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}