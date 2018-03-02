from rest_framework.serializers import *
from api.models import *
from django.contrib.auth.models import User

class ForexSerializer(ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        model = Forex
        fields = ('id','timestamp', 'opening', 'high', 'low', 'closing')

class ItemDataSerializer(ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    
    class Meta:
        model = Gdax
        fields = ('id','timestamp', 'opening', 'high', 'low', 'closing', 'volume')

class ItemSerializer(ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        model = Item
        fields = ('id', 'name', 'source', 'inst_type')

class UserSerializer(ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

class PortfolioSerializer(ModelSerializer):
    """Portfolio serializer"""
    user_id = SerializerMethodField()
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        """Map this serializer to the default portfolio model."""
        model = Portfolio
        fields = ('id','name','user_id','items')

    def get_user_id(self, obj):
        return obj.user.id

class PortfolioItemSerializer(ModelSerializer):
    """Portfolio serializer"""
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        """Map this serializer to the default portfolio model."""
        model = Portfolio
        fields = ('items',)
