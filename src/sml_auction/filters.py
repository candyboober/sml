from django.utils import timezone

from rest_framework import filters

from sml_auction.models import Auction


class AuctionFilter(filters.FilterSet):
    status = filters.django_filters.CharFilter(method='get_by_status')

    def get_by_status(self, queryset, name, value):
        if value == 'is_active':
            return queryset.filter(finish_datetime__gt=timezone.now())
        elif value == 'is_finished':
            return queryset.filter(finish_datetime__lt=timezone.now())

    class Meta:
        model = Auction
        fields = ('status', )
