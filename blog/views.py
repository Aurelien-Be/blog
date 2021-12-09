from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post
from .forms import CommentForm

# Create your views here.   
#A view function, or “view” is a Python function 
# that takes a web request and returns a web response

#def starting_page(request):
#    latest_posts = Post.objects.all().order_by("-date")[:3]
#    return render(request, "blog/index.html", {
#        "posts": latest_posts 
#    }
    
#    ) 
#in class based view:

class StartingPageView(ListView): 
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts" #to be fetched in the template

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data 


#with the url / we render the index.html file
#we don't have to precise the folder "template" in the path because we added it in templates dir 
#the function is made to expose only the 3 last posts in the index page
#we had to make the def getdate function, so to extract the data with sorted(key=)

#def posts(request):
#    all_posts = Post.objects.all().order_by("-date")
#    return render(request, "blog/all-posts.html", {
#        "all_posts": all_posts
#    } )
#with the url /posts we render the all-posts.hml file
#in class based view:

class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts" 
    ordering = ["-date"]

#def post_detail(request, slug):
#    identified_post = get_object_or_404(Post, slug=slug)
#    return render(request, "blog/post-detail.html", {
#             "post": identified_post,
             #to have a list that is usefull on our template
#             "post_tags": identified_post.tags.all()
#    } ) 
#in class based view:
class PostDetailView(DetailView):
    template_name =  "blog/post-detail.html"   
    model = Post
    #this class view is able to search by a slug
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        #then we add the comment feature
        context["comment_form"] = CommentForm() #then we can call the form in the template
        return context