from django.db import transaction
from django.utils import timezone

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import detail_route

from rest_framework.response import Response
from rest_framework import status

from sml_auction.models import Auction
from sml_auction.serializers import AuctionSerializer, BetSerializer
from sml_auction.filters import AuctionFilter


class AuctionApi(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Auction.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = AuctionSerializer
    filter_class = AuctionFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route(methods=['POST'], serializer_class=BetSerializer)
    def bet(self, request, pk=None):
        auction_item = self.queryset[0]

        if auction_item.finish_date < timezone.now():
            return Response('Auction is finished',
                            status=status.HTTP_400_BAD_REQUEST)

        if auction_item.owner.id == request.user.id:
            return Response('Auction\'s owner can\'t make bet',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data.get('value')
            if not auction_item.current_bet:
                if value < auction_item.start_price + auction_item.bet_step:
                    return Response('Bet is low, sook for a bet\'s step',
                                    status=status.HTTP_400_BAD_REQUEST)

                self.save_bet(serializer, auction_item)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            if value < auction_item.current_bet.value + auction_item.bet_step:
                return Response('Bet is low, sook for a bet\'s step',
                                status=status.HTTP_400_BAD_REQUEST)

            self.save_bet(serializer, auction_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_bet(self, bet_serializer, auction):
        with transaction.atomic():
            bet = bet_serializer.save(owner=self.request.user)
            auction.current_bet = bet
            auction.save()
