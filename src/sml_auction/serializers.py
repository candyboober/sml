from rest_framework import serializers

from sml_auction.models import Auction, Bet
from sml_auth.serializers import UserSerializer


class BetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Bet
        fields = ('id', 'owner', 'value', 'auction')


class AuctionSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    current_bet = BetSerializer(required=False)
    bets = BetSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = ('id', 'name', 'description', 'start_price', 'bet_step',
                  'finish_datetime', 'created', 'owner', 'current_bet', 'bets')
