import pytest

# Import project config
from config.config import Config

# Import project utilities
from utilities.server import Server


@pytest.mark.display_name("FTPS password login - DEV env")
def test_dev():
    status, message = Server.verify_tfs_ftps_password(host=Config.dev_tfs_host,
                                                      user_id=Config.dev_participant_password_user_id,
                                                      password=Config.dev_participant_password_password)
    if status:
        print(message)
        assert True, message
    else:
        assert False, message


@pytest.mark.display_name("FTPS password login - DEV-INT env")
def test_dev_int():
    status, message = Server.verify_tfs_ftps_password(host=Config.dev_int_tfs_host,
                                                      user_id=Config.dev_int_participant_password_user_id,
                                                      password=Config.dev_int_participant_password_password)
    if status:
        print(message)
        assert True, message
    else:
        assert False, message


@pytest.mark.display_name("FTPS password login - TEST env")
def test_test():
    status, message = Server.verify_tfs_ftps_password(host=Config.test_tfs_host,
                                                      user_id=Config.test_participant_password_user_id,
                                                      password=Config.test_participant_password_password)
    if status:
        print(message)
        assert True, message
    else:
        assert False, message


@pytest.mark.display_name("FTPS password login - STAGING env")
def test_staging():
    status, message = Server.verify_tfs_ftps_password(host=Config.staging_tfs_host,
                                                      user_id=Config.staging_participant_password_user_id,
                                                      password=Config.staging_participant_password_password)
    if status:
        print(message)
        assert True, message
    else:
        assert False, message
