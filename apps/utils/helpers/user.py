class UserAuthHelpers:
    @staticmethod
    def get_password_reset_token_cache_reference(token):
        return f"PASSWORD_RESET_TOKEN_{token}"

    @staticmethod
    def get_email_verification_token_cache_reference(token):
        return f"EMAIL_VERIFICATION_TOKEN_{token}"