from rest_framework import serializers

from .models import StockItem, StockLocation


class StockItemSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for a StockItem
    """

    class Meta:
        model = StockItem
        fields = ('url',
                  'part',
                  'supplier_part',
                  'location',
                  'quantity',
                  'status',
                  'purchase_cost',
                  'estimated_price',
                  'purchase_date',
                  'notes',
                  'updated',
                  'stocktake_date',
                  'stocktake_user',
                  'review_needed',
                  'expected_arrival')

        """ These fields are read-only in this context.
        They can be updated by accessing the appropriate API endpoints
        """
        read_only_fields = ('stocktake_date',
                            'stocktake_user',
                            'updated',
                            #'quantity',
                            )


class StockQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = StockItem
        fields = ('quantity',)


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """ Detailed information about a stock location
    """

    class Meta:
        model = StockLocation
        fields = ('url',
                  'name',
                  'description',
                  'parent',
                  'path')
