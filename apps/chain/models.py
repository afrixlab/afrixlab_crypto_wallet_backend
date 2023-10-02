from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils import enums


class Chain(enums.BaseModelMixin):
    id = models.IntegerField(
        _("Blockchain Chain ID"),
        null=False,
        blank=False,
        primary_key=True
    )
    testnet_id =  models.IntegerField(
        _("Blockchain Testnet Chain ID"),
        null=True,
        blank=True,
        unique=True,
        default=0
    )
    chain_name = models.CharField(
        _("Blockchain Name"),
        null=False,
        blank=False,
        max_length=35
    )
    chain_symbol = models.CharField(
        _("Blockchain Symbol"),
        null=False,
        blank=False,
        max_length=15
    )
    chain_type = models.CharField(
        _("Blockchain Consenesus Type"),
        choices=enums.BlockchainConsensusType.choices(),
        default=enums.BlockchainConsensusType.PROOF_OF_STAKE.value,
        null=False,
        blank=False,
        max_length=15
    )
    chain_logo = models.FileField(
        _("Blockchain Logo"),
        null=False,
        blank=False,
        upload_to="vaults/chain/"
    )
    chain_explorer =models.URLField(
        _("Blockchain Explorer URL"),
        null=True,
        blank=True,
        max_length=125,
    )
    testnet_explorer =models.URLField(
        _("Blockchain Testnet Explorer URL"),
        null=True,
        blank=True,
        max_length=125,
    )
    class Meta:
        verbose_name = _("Supported Blockchain")
        verbose_name_plural = _("Supported Blockchains")
    
    def __str__(self):
        return f"{self.chain_name} {self.chain_symbol}"
    
    
class ChainNodes(enums.BaseModelMixin):
    
    chain = models.ForeignKey(
        Chain,
        verbose_name = _("Blockchain that owns this node"),
        on_delete=models.CASCADE
    )
    node = models.URLField(
        null=False,
        blank=False,
        max_length=255
    )
    node_chain_type = models.CharField(
        _("Blockchain Node Type"),
        choices= enums.NodeType.choices(),
        default=enums.NodeType.TESTNET.value,
        max_length=10
    ) 
    class Meta:
        verbose_name = _("Blockchain node")
        verbose_name_plural = _("Blockchain nodes")


    def __str__(self):
        return self.node
    
    
class Coin(enums.BaseModelMixin):
    coin_chain = models.ForeignKey(
        Chain,
        on_delete=models.CASCADE,
        verbose_name= _("Blockchain coin was deployed or created")
    )
    coin_name = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        verbose_name= _("Coin Name"),
        unique=True
    )
    coin_symbol = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        verbose_name= _("Coin Symbol"),
        unique=True
    )
    coin_logo = models.FileField(
        _("Coin Logo"),
        null=False,
        blank=False,
        upload_to="vaults/coin/"
    )
    contract_address = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        verbose_name= _("Contract address of coin")
    )
    
    class Meta:
        verbose_name = 'Blockchain Coin'
        verbose_name_plural = 'Blockchain Coins'
        
    def __str__(self):
        return self.coin_name