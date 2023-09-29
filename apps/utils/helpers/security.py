import secrets


class Token:
    @staticmethod
    def create_random_hex_token(no_of_bytes=16):
        # Create random 16 bytes hex token
        return secrets.token_hex(no_of_bytes)

    @staticmethod
    def create_otp(no_of_digits=6):
        # Create random 16 bytes hex token
        return "".join(str(secrets.randbelow(10)) for i in range(no_of_digits))
