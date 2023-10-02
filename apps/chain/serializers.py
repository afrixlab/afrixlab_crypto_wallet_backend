from rest_framework import serializers
from apps.chain.models import Chain,Coin

class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        fields = "__all__"
        ref_name = "Chain - List"
            



class CoinSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coin
        fields = "__all__"
        ref_name = "Coin - List"

    class Create(serializers.ModelSerializer):
        class Meta:
            model = Coin
            fields = "__all__"
            ref_name = "Coin - Create"

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = Coin
            fields = "__all__"
            ref_name = "Coin - Retrieve"
