from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from supplier.models import SupplierPart
from part.models import Part
from InvenTree.models import InvenTreeTree

from datetime import datetime


class StockLocation(InvenTreeTree):
    """ Organization tree for StockItem objects
    """

    @property
    def items(self):
        stock_list = self.stockitem_set.all()
        return stock_list


class StockItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='locations')
    supplier_part = models.ForeignKey(SupplierPart, blank=True, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    updated = models.DateField(auto_now=True)

    # last time the stock was checked / counted
    stocktake_date = models.DateField(blank=True, null=True)
    stocktake_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    review_needed = models.BooleanField(default=False)
    
    #MY ADDITIONS
    purchase_cost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    #END MY

    # Stock status types
    ITEM_IN_STOCK = 10
    ITEM_INCOMING = 15
    ITEM_IN_PROGRESS = 20
    ITEM_COMPLETE = 25
    ITEM_ATTENTION = 50
    ITEM_DAMAGED = 55
    ITEM_DESTROYED = 60

    ITEM_STATUS_CODES = {
        ITEM_IN_STOCK: _("In stock"),
        ITEM_INCOMING: _("Incoming"),
        ITEM_IN_PROGRESS: _("In progress"),
        ITEM_COMPLETE: _("Complete"),
        ITEM_ATTENTION: _("Attention needed"),
        ITEM_DAMAGED: _("Damaged"),
        ITEM_DESTROYED: _("Destroyed")
    }

    status = models.PositiveIntegerField(
        default=ITEM_IN_STOCK,
        choices=ITEM_STATUS_CODES.items(),
        validators=[MinValueValidator(0)])

    notes = models.CharField(max_length=100, blank=True)

    # If stock item is incoming, an (optional) ETA field
    expected_arrival = models.DateField(null=True, blank=True)

    infinite = models.BooleanField(default=False)

    # History of this item
    history = HistoricalRecords()

    @transaction.atomic
    def stocktake(self, count, user):
        """ Perform item stocktake.
        When the quantity of an item is counted,
        record the date of stocktake
        """

        count = int(count)

        if count < 0 or self.infinite:
            return

        self.quantity = count
        self.stocktake_date = datetime.now().date()
        self.stocktake_user = user
        self.save()

    @transaction.atomic
    def add_stock(self, amount):
        """ Add items to stock
        This function can be called by initiating a ProjectRun,
        or by manually adding the items to the stock location
        """

        amount = int(amount)

        if self.infinite or amount == 0:
            return

        amount = int(amount)

        q = self.quantity + amount
        if q < 0:
            q = 0

        self.quantity = q
        self.save()

    @transaction.atomic
    def take_stock(self, amount):
        self.add_stock(-amount)

    def __str__(self):
        return "{n} x {part} @ {loc}".format(
            n=self.quantity,
            part=self.part.name,
            loc=self.location.name)
