from django.db import models
from django.contrib.postgres.fields import JSONField  

SECONDARY_RECIPES = {
    "Plank": {"Wood": 1, "Iron": 1},
    "Brick": {"Clay": 1, "Water": 1},
    "Steel": {"Iron": 1, "Crystal": 1}
}

FINAL_RECIPES = {
    "Sword": {
        "required": {"Plank": 1, "Steel": 1},
        "points": 2
    },
    "House": {
        "required": {"Plank": 1, "Brick": 1, "Water": 1},
        "points": 3
    },
    "Factory": {
        "required": {"Brick": 1, "Steel": 1, "Iron": 1},
        "points": 4
    }
}


def default_primary_cards():
    # Primary resources with initial count 0.
    return {"Wood": 0, "Iron": 0, "Clay": 0, "Water": 0, "Crystal": 0}

def default_secondary_cards():
    return {"Plank": 0, "Brick": 0, "Steel": 0}

def default_final_products():
    return {"Sword": 0, "House": 0, "Factory": 0}


class Player(models.Model):
    name = models.CharField(max_length=100)
    wallet = models.IntegerField(default=1000)
    points = models.IntegerField(default=0)
    knights = models.IntegerField(default=0)
    # Inventories stored as JSON data.
    primary_cards = models.JSONField(default=default_primary_cards)
    secondary_cards = models.JSONField(default=default_secondary_cards)
    final_products = models.JSONField(default=default_final_products)

    def __str__(self):
        return self.name


class Card(models.Model):
    CARD_TYPE_CHOICES = [
        ('PRIMARY', 'Primary'),
        ('SECONDARY', 'Secondary'),
        ('FINAL', 'Final'),
        ('CHANCE', 'Chance'),
    ]
    name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    image_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class AuctionItem(models.Model):
    seller = models.ForeignKey(Player, related_name='auction_items', on_delete=models.CASCADE)
    resource = models.CharField(max_length=50)  # Primary resource name (e.g., "Wood")
    base_price = models.IntegerField()
    current_bid = models.IntegerField(default=0)
    highest_bidder = models.ForeignKey(
        Player, related_name='bids', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.resource} from {self.seller.name} (Current Bid: {self.current_bid})"


class BuyOrder(models.Model):
    buyer = models.ForeignKey(Player, related_name='buy_orders', on_delete=models.CASCADE)
    resource = models.CharField(max_length=50)  
    offered_price = models.IntegerField()      

    def __str__(self):
        return f"Buy {self.resource} at {self.offered_price} by {self.buyer.name}"


class SellerOffer(models.Model):
    buy_order = models.ForeignKey(BuyOrder, related_name='seller_offers', on_delete=models.CASCADE)
    seller = models.ForeignKey(Player, related_name='seller_offers', on_delete=models.CASCADE)
    offer_price = models.IntegerField()

    def __str__(self):
        return f"Offer by {self.seller.name} for {self.buy_order.resource} at {self.offer_price}"

