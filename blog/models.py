from django.db import models 
from django.db.models.deletion import SET_NULL
from django.core.validators import MinLengthValidator




# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)
#to show the tag in admin/blog/tag/ and not "objects"
    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    emailadress = models.EmailField()
    
    #to show the full name in /admin/blog/author/
    def full_name(self):
        return f"{self.first_name} {self.name}"

    def __str__(self):
        return self.full_name()

#Title, Exercpt, Image Name, Date, Slug, Content
class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=250)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title  #to diplay the title in comments section instead of post object

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    
