from rest_framework.serializers import *
from rest_framework_bulk import BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from api.models import *
from django.contrib.auth.models import User

class CandlesSerializer(BulkSerializerMixin, ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    
    class Meta:
        model = Candles
        fields = ('id', 'item', 'timestamp', 'opening', 'high', 'low', 'closing', 'volume')
        list_serializer_class = BulkListSerializer

    #def create(self, validated_data):
    #    candlestick, created = Candles.objects.get_or_create(
    #        item = validated_data['item'],
    #        timestamp = validated_data['timestamp'],
    #        defaults={
    #            'opening' : validated_data['opening'],
    #            'high' : validated_data['high'],
    #            'low' : validated_data['low'],
    #            'closing' : validated_data['closing'],
    #            'volume' : validated_data['volume']}
    #        )
    #    return candlestick

class PredictionsSerializer(ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        model = Predictions
        fields = ('id', 'item', 'timestamp', 'closing')

class ValidationsSerializer(ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        model = Validations
        fields = ('id', 'item', 'typ', 'result')

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
