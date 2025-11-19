import pyotp

# Import project configs
from configs.config import Config

# Import project utilities
from utilities.logger import get_logger

# Get module-level logger
logger = get_logger(__name__)


class TOTP:
    @staticmethod
    def generate_totp() -> str:
        secret = Config.okta_jh_email_totp_secret

        if not secret:
            e_message = "TOTP secret missing."
            logger.error(e_message)
            raise RuntimeError(e_message)

        try:
            totp = pyotp.TOTP(secret)
            logger.info("Generated TOTP successfully.")
            return totp.now()
        except Exception as e:
            e_message = f"Failed to generate TOTP code: {e}"
            logger.error(e_message)
            raise RuntimeError(e_message) from e
