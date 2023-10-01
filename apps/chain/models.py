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
        max_length=4
    )
    chain_logo = models.FileField(
        _("Blockchain Logo"),
        null=False,
        blank=False,
        upload_to="vaults/chain/"
    )
    chain_nodes = models.ManyToManyField(
        to="ChainNodes",
        verbose_name= _("Blockchain Nodes"),
        blank=False,
        null=False
    )
    
    class Meta:
        verbose_name = _("Supported Blockchain")
        verbose_name_plural = _("Supported Blockchains")
    
    def __str__(self):
        return self.chain_name
    
    
class ChainNodes(enums.BaseModelMixin):
    node = models.URLField(
        unique=True,
        null=False,
        blank=False,
        max_length=255
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
        verbose_name= _("Contract address of coin")
    )
    
    class Meta:
        verbose_name = 'Blockchain Coin'
        verbose_name_plural = 'Blockchain Coins'
        
    def __str__(self):
        return self.coin_name