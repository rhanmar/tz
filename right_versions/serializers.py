from rest_framework import serializers

from deals.models import Deal, Customer, Item


class TopCustomersSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField()
    username = serializers.CharField()
    gems = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        allow_empty=True,
        required=False
        )

    class Meta:
        model = Deal
        fields = ['spent_money', 'username', 'gems']
