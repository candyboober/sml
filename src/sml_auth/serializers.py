from rest_framework import serializers

from sml_auction.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('username', )
