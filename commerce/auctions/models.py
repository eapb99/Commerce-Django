from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return  f'{self.username}'

class Category(models.Model):
    code = models.CharField(max_length=8, unique=True, null=True, blank=True)
    name = models.CharField(max_length=32, unique=True, null=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    image = models.URLField(max_length=1000)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']

class Listing(models.Model):
    lis_name = models.CharField(max_length=50, verbose_name='name')
    lis_description = models.TextField(max_length=500, verbose_name='description')
    lis_image = models.CharField(max_length=500, verbose_name='image')
    lis_active = models.BooleanField(default=True, verbose_name='active')
    lis_date = models.DateTimeField(auto_now=True, verbose_name='date')
    lis_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2, verbose_name='price')
    lis_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user", blank=True, verbose_name='User')
    category = models.ManyToManyField(Category, blank=True, related_name="listing_category")
    watchlist = models.ManyToManyField(User, related_name='watchlist', blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.lis_name}"

    def get_categories(self):
        return ", ".join([str(p) for p in self.category.all()])

class Bid(models.Model):
    initial = models.DecimalField(max_digits=6, decimal_places=2,default=0,validators=[MinValueValidator(0.01)])
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listings")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

    def __str__(self):
        return f'{self.initial} {self.listings} {self.user} hola'


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

