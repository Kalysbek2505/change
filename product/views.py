from django.http import QueryDict
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, filters
from rest_framework.decorators import action, api_view
from loguru import logger
import os
import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Product, Category, Comment, Like, Rating, Favoritos
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, FavoritosSerializer
from .permissions import IsAuthor


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    @swagger_auto_schema(manual_parameters=[openapi.Parameter('category', openapi.IN_QUERY, 'recommendations by categories', type=openapi.TYPE_STRING, required=True)])
    @action(methods=['GET'], detail=False)
    def recommendation(self, request):
        cat_title = request.query_params.get('category')
        categories = Category.objects.get(title__icontains=cat_title)
        queryset = self.get_queryset()
        queryset = queryset.filter(categories=categories)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, 200)

    # @swagger_auto_schema(manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, 'search Product by name', type=openapi.TYPE_STRING)])

    

    @action(methods=['GET'], detail=False)
    def search(self, request):
        name = request.query_params.get('title')
        queryset = self.get_queryset()
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)

   
    @action(methods=['GET'], detail=False)
    def order_by_rating(self, request):
        queryset = self.paginate_queryset()
        queryset = sorted(queryset, key=lambda product: product.average_rating, reverse=True)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, 200)

    



class CategoryViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



@api_view(['GET'])
def toggle_like(request, a_id):
    user = request.user
    product = get_object_or_404(Product, id=a_id)

    if Like.objects.filter(user=user, product=product).exists():
        Like.objects.filter(user=user, product=product).delete()
    else:
        Like.objects.create(user=user, product=product)
    return Response("Like toggled", 200)


@api_view(['POST'])
def add_rating(request, a_id):
    user = request.user
    product = get_object_or_404(product, id=a_id)
    value = request.POST.get('value')

    if not user.is_authenticated:
        raise ValueError("Authentication credentials are not provided")

    if not value:
        raise ValueError("Value is required")

    if Rating.objects.filter(user=user, product=product).exists():
        rating = Rating.objects.get(user=user, product=product)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user,product=product, value=value)

def add_to_favoritos(request, a_id):
    user = request.user
    product = get_object_or_404(product, id=a_id)

    if Favoritos.objects.filter(user=user, product=product).exists():
        Favoritos.objects.filter(user=user, product=product).delete()
    else:
        Favoritos.objects.create(user=user, product=product)
    return Response("added to favoritos", 200)


class FavoritosViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Favoritos.objects.all()
    serializer_class = FavoritosSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

   
    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset









# class TradeViewSet(ModelViewSet):
#     queryset = Trade.objects.all()
#     serializer_class = TradeSerializer
#     permission_classes = [IsAuthenticated]


log = logger.__getattribute__('log')

def index(request):
    log.warning('Message for Warning')
    log.error('Message for Error')
    log.critical('Message for critical problem')
    log.information('Message for information')
    log.debug('Message for debug')
    return render(request, 'product/index.html')
    

