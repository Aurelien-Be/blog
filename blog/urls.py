from django.urls import path, reverse

from . import views
#import the views file in order to connect the requests to the paths 

urlpatterns = [
    path('', views.starting_page, name='starting-page'),
    path('posts', views.posts, name='posts-page'),
    path('posts/<slug:slug>', views.post_detail, name='post-detail-page') #/posts/my-first-post
]

# signs <> in order to have a dynamic url 
#we add a name for each path because it's easier to 
#we can refer to them by the name rather than by the url. 
# That way, if the url changes in the app, you only need to update the code in one place (the urls.py module). 