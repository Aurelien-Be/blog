from django.db import models 
from django.db.models.deletion import SET_NULL
from django.core.validators import MinLengthValidator




# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)

class Author(models.Model):
    first_name = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    emailadress = models.EmailField()

#Title, Exercpt, Image Name, Date, Slug, Content
class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=250)
    image_name = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    tags = models.ManyToManyField(Tag)


