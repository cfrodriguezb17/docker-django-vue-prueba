from .models import User, Transaction
from rest_framework import serializers
from django.core.validators import MinLengthValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email', 
            'first_name', 
            'password',
            'points',
            'is_admin',
            'created_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [MinLengthValidator(6, message="La contraseña debe tener al menos 6 caracteres.")]}
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'amount',
            'transaction_type',
            'description',
            'created_at'
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 
            'first_name', 
            'points',
            'is_admin',
            'created_at'
        ]

class RedeemPointsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=29,
        decimal_places=2,
        min_value=1
    )
    description = serializers.CharField(required=False, allow_blank=True, max_length=200)

class GrantPointsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(
        max_digits=29,
        decimal_places=2,
        min_value=1
    )
    description = serializers.CharField(required=False, allow_blank=True, max_length=200)

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("El usuario especificado no existe.")
        return value
    