from rest_framework import serializers
from apps.chain.models import Chain,Coin

class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        exclude = [
            "date_added",
            "date_last_modified"
        ]
        ref_name = "Chain - List"
            



class CoinSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coin
        exclude = [
            "date_added",
            "date_last_modified"
        ]
        ref_name = "Coin - List"
