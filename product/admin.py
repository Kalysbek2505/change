from django.contrib import admin

from django.contrib import admin

from .models import Category, Product, Comment, Rating, Like, Favoritos

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favoritos)