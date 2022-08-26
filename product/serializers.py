from rest_framework import serializers

from .models import Product, Comment, Category, Rating, Like, Favoritos


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['ratings'] = instance.average_rating
        rep['likes'] = instance.likes.all().count()
        rep['liked_by_user'] = False
        rep['user_rating'] = 0

        request = self.context.get('request')
        if request.user.is_authenticated:
            rep['liked_by_user'] = Like.objects.filter(user=request.user, product=instance).exists()
            if Rating.objects.filter(user=request.user,product=instance).exists():
                rating = Rating.objects.get(user=request.user,product=instance)
                rep['user_rating'] = rating.value

        return rep

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        return rep

class FavoritosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoritos
        exclude = ['user']
