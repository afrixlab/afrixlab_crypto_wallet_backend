from django.conf import settings
from mnemonic import Mnemonic


class WalletClient:
    mnemo = Mnemonic("english")
    
    def generate_mnemonic_phrase(self):
        return self.mnemo.generate(strength=256)
    
a = WalletClient().generate_mnemonic_phrase()
print(a)