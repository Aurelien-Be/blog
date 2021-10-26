from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.   
#A view function, or “view” is a Python function 
# that takes a web request and returns a web response

def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {
        "posts": latest_posts 
    }
    
    ) 
#with the url / we render the index.html file
#we don't have to precise the folder "template" in the path because we added it in templates dir 
#the function is made to expose only the 3 last posts in the index page
#we had to make the def getdate function, so to extract the data with sorted(key=)

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    } )
#with the url /posts we render the all-posts.hml file

def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
             "post": identified_post,
             #to have a list that is usefull on our template
             "post_tags": identified_post.tags.all()
    } ) 