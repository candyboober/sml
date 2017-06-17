import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from sml_auction.models import Auction, Bet
from sml_auction.tasks import (send_auction_created_email,
                               send_bet_created_email)


@receiver(post_save, sender=Auction, dispatch_uid=uuid.uuid4().hex)
def auction_created_notification(sender, instance, **kwargs):
    send_auction_created_email.delay(instance.id)

@receiver(post_save, sender=Bet, dispatch_uid=uuid.uuid4().hex)
def new_bet_notification(sender, instance, **kwargs):
    send_bet_created_email.delay(instance.auction.id)
