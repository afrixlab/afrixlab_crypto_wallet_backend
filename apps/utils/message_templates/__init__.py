from django.conf import settings
from apps.utils.helpers.commons import DateTime


class MessageTemplates:
    @staticmethod
    def otp(name, otp):
        return f"""
        {name.title() + ', ' if name else ''}Your One-Time-Password is {otp}.
        """

    @staticmethod
    def password_reset_email(token: str, page_base_url=None):
        link = f"{page_base_url or settings.PASSWORD_RESET_PAGE}/{token}"
        buttonText = "Reset Password"

        message = f"""
            <p style="color: #fff">Kindly click the link below to continue in resetting your account password.</p>
            <p style="color: #fff"><a href="{page_base_url or settings.PASSWORD_RESET_PAGE}/{token}">{page_base_url or settings.PASSWORD_RESET_PAGE}/{token}</a></p>
            <p style="color: #fff"><b>The above link will expire in {DateTime.convert_seconds_to_hr_min(settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS)}.</b></p>
            """
        return message

    @staticmethod
    def email_verification_email(token: str, page_base_url: str):
        link = f"{page_base_url}/{token}"
        buttonText = "Verify Email"

        message = f"""
                <p style="color: #fff">Kindly click the link below to continue in verifying your account email.</p>
                <p style="color: #fff"><a href="{page_base_url}/{token}">{page_base_url}/{token}</a></p>
                <p style="color: #fff"><b>The above link will expire in {DateTime.convert_seconds_to_hr_min(settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS)}.</b></p>
                """
        return message

    @staticmethod
    def email_verification_success():
        message = f"""
                <p style="color: #fff">Your email has been verified successfully.</p>
                """
        return message

    @staticmethod
    def email_otp_withdrawal_email(token: str):
        message = f"""
                    <p style="color: #fff">Kindly verify your email with the code below</p>
                    <h1 style="color: #fff">{token}</h1>
                    <p style="color: #fff"><b>The above code will expire in {DateTime.convert_seconds_to_hr_min(settings.EMAIL_LOGIN_TOKEN_EXPIRATION_SECS)}.</b></p>
                    """
        return message


    @staticmethod
    def withdrawal_request_accepted(withdrawal_request_instance):
        message = f"""
                    <p class=''>Your withdrawal of  {withdrawal_request_instance.amount} {withdrawal_request_instance.currency_iso3} has been accepted, payment will follow shortly.</p>
                """
        return message

    @staticmethod
    def withdrawal_request_rejected(withdrawal_request_instance):
        message = f"""
                    <p style="color: #fff">Your withdrawal request has been rejected.</p>
                """
        return message
    


    