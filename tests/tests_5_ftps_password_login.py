import pytest

# Import project configs
from configs.config import Config

# Import project utilities
from utilities.server import Server
from utilities.logger import get_logger

# Get module-level logger
logger = get_logger(__name__)


@pytest.mark.display_name("FTPS password login - DEV env")
def test_dev():
    status, message = Server.verify_tfs_ftps_password(host=Config.dev_tfs_host,
                                                      user_id=Config.dev_participant_password_user_id,
                                                      password=Config.dev_participant_password_password)
    assert_test(status, message)


@pytest.mark.display_name("FTPS password login - DEV-INT env")
def test_dev_int():
    status, message = Server.verify_tfs_ftps_password(host=Config.dev_int_tfs_host,
                                                      user_id=Config.dev_int_participant_password_user_id,
                                                      password=Config.dev_int_participant_password_password)
    assert_test(status, message)


@pytest.mark.display_name("FTPS password login - TEST env")
def test_test():
    status, message = Server.verify_tfs_ftps_password(host=Config.test_tfs_host,
                                                      user_id=Config.test_participant_password_user_id,
                                                      password=Config.test_participant_password_password)
    assert_test(status, message)


@pytest.mark.display_name("FTPS password login - STAGING env")
def test_staging():
    status, message = Server.verify_tfs_ftps_password(host=Config.staging_tfs_host,
                                                      user_id=Config.staging_participant_password_user_id,
                                                      password=Config.staging_participant_password_password)
    assert_test(status, message)


def assert_test(status, message) -> None:
    if status:
        logger.info(message)
        assert True
    else:
        logger.error(message)
        assert False, message
