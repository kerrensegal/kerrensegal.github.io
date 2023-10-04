from django.contrib.auth.models import AbstractUser
from django.db import models

categories = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('sports', 'Sports'),
    ('pets', 'Pets'),
    ('books', 'Books'),
    ('music', 'Music'),
    ('art', 'Art'),
    ('health', 'Health'),
    ('business', 'Business')
]

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=categories, blank=True)
    image = models.URLField(blank=True)

# class Bid():

# class Comment():
