import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.template.loader import get_template
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from model_utils.models import TimeStampedModel

from sml_auth.models import User
from sml_auction.emails import auction_email_notification


def default_finish_date():
    return timezone.now() + datetime.timedelta(days=2)


class Auction(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=40)
    description = models.CharField(_('Description'), max_length=1000,
                                   blank=True)
    # if price will be greater then 2 billions
    # we have to migrate to BigInteger
    start_price = models.PositiveIntegerField(
        _('Start price'),
        validators=(MinValueValidator(1), MaxValueValidator(2000000000)))
    bet_step = models.PositiveIntegerField(
        _('Bet step'),
        validators=(MinValueValidator(1), MaxValueValidator(2000000000)))
    finish_datetime = models.DateTimeField(
        _('Finish time'),
        default=default_finish_date
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_('Owner'),
                              related_name='auctions')
    current_bet = models.OneToOneField('Bet',
                                       verbose_name=_('Bet'),
                                       related_name='active_item',
                                       null=True)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('Winner'),
                               related_name='auctions_success',
                               null=True)
    finished = models.BooleanField(_('Finished'), default=False)


    @classmethod
    def send_auction_created_email(cls, author_id):
        query = get_user_model().objects.exclude(
            email__isnull=True,
            email__exact='',
            id=author_id).only('email').values('email')
        emails = (e['email'] for e in query.values())

        url = reverse('api:auction-detail', args=[str(author_id)])
        url = settings.SITE_IRL + url

        auction_email_notification(emails, url, 'new_auction',
                                   'New auction has been registered')

    @classmethod
    def send_auction_finished_emails(cls):
        auctions = cls.objects.filter(finished=False,
                                      finish_datetime__gt=timezone.now())
        if not auctions:
            return

        for auc in auctions:
            auc.winner = auc.current_bet.owner
            auc.save()

        author_ids = [a.owner.id for a in auctions]

        for author_id in author_ids:
            cls.send_auction_created_email(author_id)

    @classmethod
    def send_auction_finished_email(cls, author_id):
        query = get_user_model().objects.exclude(
            email__isnull=True,
            email__exact='',
            id=author_id).only('email').values('email')
        emails = (e['email'] for e in query.values())

        url = reverse('api:auction-detail', args=[str(author_id)])
        url = settings.SITE_IRL + url

        auction_email_notification(emails, url, 'auction_finished',
                                   'Auction has been finished')


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Auction slot'


class Bet(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_('Owner'),
                              related_name='bets')
    value = models.PositiveIntegerField(_('Value'))
    auction = models.ForeignKey(Auction,
                                verbose_name=_('Auction'),
                                related_name='bets')

    @classmethod
    def new_bet_send_email(self, auction_id):
        emails = Bet.objects \
            .filter(auction_id=auction_id) \
            .select_related('owner') \
            .values_list('owner__email', flat=True).distinct()

        author_id = Auction.objects.select_related('owner') \
            .get(id=auction_id).owner.id
        url = reverse('api:auction-detail', args=[str(author_id)])
        url = settings.SITE_IRL + url

        auction_email_notification(emails, url, 'new_bet',
                                   'New bet has been registered')

    def __str__(self):
        return 'bet {} by {}'.format(self.id, self.auction.name)

    class Meta:
        verbose_name = _('Bet')
