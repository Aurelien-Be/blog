from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse #allows to construct urls automatically by just using the names of the urls 
from django.views.generic import ListView
from django.views import View 
from django.db.models import Q 

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

class StartingPageView(ListView):  #render 3 article in the index 
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts" #to be fetched in the template

    def get_queryset(self):  #to return only 3 posts in the main page
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

class PostsView(ListView): #render articles
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
class PostDetailView(View): #render a single article

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_save_for_later = post_id in stored_posts
        else:
            is_save_for_later = False

        return is_save_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by('-created'), #fetch the comments, in order to show them 
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context )
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug) #we fetch the post

        if comment_form.is_valid():
            comment = comment_form.save(commit=False) 
            #commit=False creates a new object and don't hit the database. In the CommentForm, we exclude the Post field, so it would cause pb without it 
            comment.post = post #set the postfield to the post wich the commment should be related
            comment.save() #we can call save because its come from Forms, it is connected to the database

            return HttpResponseRedirect(reverse('post-detail-page', args=[slug])) 
         
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by('-created'),
             "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context )


class SearchView(ListView):  #search articles into the blog
    model = Post
    template_name= "blog/searcharticle.html"
    context_object_name= 'search_article'
    paginate_by = 10
    ordering = ["-date"]
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )       
        
        return object_list.order_by('-date')
    

class ReadLaterView(View): #save an article during a session with cookies

    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"]= posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts') #.get to not have an error if there is no stored posts

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST['post_id'])
        
        if post_id not in stored_posts:
          stored_posts.append(post_id)
          
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect('/')


        
    







