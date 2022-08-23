from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=50)
     
    def __str__(self):
        return self.title

class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name='product')
    title = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0

class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'LIKE TO Product: {self.product}  FROM USER: {self.user}'




class Favoritos(models.Model):
    user = models.ForeignKey(User, related_name='favoritos', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favoritos', on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])

    def __str__(self):
        return f'{self.user}: {self.product}. Rating: {self.value}'

class Trade(models.Model):
    user = models.ManyToManyField(User, related_name='changes')
    # user1 = models.ManyToManyField(User, related_name='changes')
    product = models.ManyToManyField(Product, related_name='changes')
    # product1 = models.ManyToManyField(Product, related_name='changes')