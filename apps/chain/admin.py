from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from .models import Chain,ChainNodes,Coin


@admin.register(Chain)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Chain info"),
            {
                "fields": (
                    "id",
                    "chain_name",
                    "chain_symbol",
                    "testnet_id",
                    "chain_type"     
                )
            },
        ),
        
        (
            _("Meta Information"),
            {
                "fields": (
                    "testnet_explorer",
                    "chain_explorer",
                )
            },
        ),
        
    )
    list_display = [
        "id",
        "chain_name",
        "chain_type",
    ]
    search_fields = ["chain_symbol", "chain_id"]



@admin.register(ChainNodes)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Chain info"),
            {
                "fields": (
                    "node_chain_type",    
                )
            },
        ),
        
        (
            _("Meta Information"),
            {
                "fields": (
                    "node",
                    "chain",
                )
            },
        ),
        
    )
    list_display = [
        "node",
        "node_chain_type",
        "chain"
    ]
    search_fields = ["node"]



