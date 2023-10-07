from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.utils.enums import (
    BaseModelMixin,
)

UserModel = get_user_model()

class Wallet(BaseModelMixin):
    owner = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_wallet",
        verbose_name=_("Wallet Owner")
    )
    balance = models.DecimalField(
        _("Wallet Balance"),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Wallet of {self.owner.username}"

class Transaction(BaseModelMixin):
    sender_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='sent_transactions',
        verbose_name=_("Sender Wallet")
    )
    recipient_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='received_transactions',
        verbose_name=_("Recipient Wallet")
    )
    amount = models.DecimalField(
        _("Transaction Amount"),
        max_digits=10,
        decimal_places=2
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Transaction Timestamp")
    )

    def __str__(self):
        return f"Transaction from {self.sender_wallet.owner.username} to {self.recipient_wallet.owner.username}"

    def save(self, *args, **kwargs):
        # Ensure the sender has enough balance before saving the transaction
        if self.sender_wallet.balance >= self.amount:
            self.sender_wallet.balance -= self.amount
            self.recipient_wallet.balance += self.amount
            self.sender_wallet.save()
            self.recipient_wallet.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Insufficient balance for this transaction")

