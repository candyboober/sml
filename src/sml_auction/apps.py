from django.apps import AppConfig


class SmlAuctionConfig(AppConfig):
    name = 'sml_auction'

    def ready(self):
        import sml_auction.signals
