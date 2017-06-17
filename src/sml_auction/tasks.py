from sml.celery import app
from sml_auction.models import Auction, Bet


@app.task(bind=True)
def send_auction_created_email(self, author_id):
    Auction.send_auction_created_email(author_id)

@app.task(bind=True)
def send_bet_created_email(self, auction_id):
    Bet.new_bet_send_email(auction_id)
