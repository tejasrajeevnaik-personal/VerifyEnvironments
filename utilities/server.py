# noinspection PyPackageRequirements
import paramiko
import ssl
from ftplib import FTP_TLS
from io import StringIO
from typing import Optional, Tuple
import time
import logging

# Import project utilities
from utilities.logger import get_logger

# Get module-level logger
logger = get_logger(__name__)


class Server:
    @staticmethod
    def verify_tfs_sftp_password(host: str,
                                 user_id: str,
                                 password: str,
                                 port: int = 22,
                                 timeout: int = 300,
                                 max_retries: int = 2,
                                 delay: int = 2) -> Tuple[bool, str]:
        paramiko_logger = logging.getLogger("paramiko")
        old_paramiko_level = paramiko_logger.getEffectiveLevel()

        message = None
        for attempt in range(1, max_retries + 1):
            ssh = sftp = None
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=host,
                    port=port,
                    username=user_id,
                    password=password,
                    timeout=timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
                sftp = ssh.open_sftp()
                # Lightweight validation - just verify connection is established and listdir is working
                sftp.listdir('.')
                message = f"SFTP (password) connected successfully on attempt {attempt}"
                paramiko_logger.setLevel(old_paramiko_level)
                return True, message
            except Exception as exception:
                message = f"SFTP (password) attempt {attempt} failed: {exception}"
                if attempt < max_retries:
                    # Comment below line if DEBUG logs are overwhelming
                    paramiko_logger.setLevel(logging.DEBUG)
                    logger.warning(message)
                    time.sleep(delay)
            finally:
                if sftp:
                    # noinspection PyBroadException
                    try:
                        sftp.close()
                    except Exception:
                        pass
                if ssh:
                    # noinspection PyBroadException
                    try:
                        ssh.close()
                    except Exception:
                        pass

        paramiko_logger.setLevel(old_paramiko_level)
        return False, message

    @staticmethod
    def verify_tfs_sftp_ssh_key(host: str,
                                user_id: str,
                                private_key_path: Optional[str] = None,
                                private_key_passphrase: Optional[str] = None,
                                private_key_text: Optional[str] = None,
                                port: int = 22,
                                timeout: int = 300,
                                max_retries: int = 1,
                                delay: int = 2) -> Tuple[bool, str]:
        paramiko_logger = logging.getLogger("paramiko")
        old_paramiko_level = paramiko_logger.getEffectiveLevel()

        message = None
        for attempt in range(1, max_retries + 1):
            ssh = sftp = None
            try:
                if private_key_path:
                    pkey = paramiko.RSAKey.from_private_key_file(private_key_path, password=private_key_passphrase)
                elif private_key_text:
                    pkey = paramiko.RSAKey.from_private_key(StringIO(private_key_text), password=private_key_passphrase)
                else:
                    e_message = "Either private key path or private key text must be provided."
                    logger.error(e_message)
                    raise ValueError(e_message)

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=host,
                    port=port,
                    username=user_id,
                    pkey=pkey,
                    timeout=timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
                sftp = ssh.open_sftp()
                # Lightweight validation - just verify connection is established and listdir is working
                sftp.listdir('.')
                message = f"SFTP (SSH key) connected successfully on attempt {attempt}"
                paramiko_logger.setLevel(old_paramiko_level)
                return True, message
            except Exception as exc:
                message = f"SFTP (SSH key) attempt {attempt} failed: {exc}"
                if attempt < max_retries:
                    # Comment below line if DEBUG logs are overwhelming
                    paramiko_logger.setLevel(logging.DEBUG)
                    logger.warning(message)
                    time.sleep(delay)
            finally:
                if sftp:
                    # noinspection PyBroadException
                    try:
                        sftp.close()
                    except Exception:
                        pass
                if ssh:
                    # noinspection PyBroadException
                    try:
                        ssh.close()
                    except Exception:
                        pass

        paramiko_logger.setLevel(old_paramiko_level)
        return False, message

    @staticmethod
    def verify_tfs_ftps_password(host: str,
                                 user_id: str,
                                 password: str,
                                 port: int = 21,
                                 timeout: int = 300,
                                 passive: bool = True,
                                 cafile: Optional[str] = None,
                                 max_retries: int = 1,
                                 delay: int = 2) -> Tuple[bool, str]:
        message = None
        enable_debug = False
        for attempt in range(1, max_retries + 1):
            ftps = None
            try:
                if cafile:
                    context = ssl.create_default_context(cafile=cafile)
                else:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                ftps = FTP_TLS(context=context)
                # If first attempt fails, enable debug mode for subsequent attempts
                if enable_debug:
                    ftps.set_debuglevel(2)
                ftps.connect(host=host, port=port, timeout=timeout)
                ftps.auth()
                ftps.login(user=user_id, passwd=password)
                ftps.prot_p()
                ftps.set_pasv(passive)
                # Lightweight validation - just verify connection is established and listdir is working
                ftps.mlsd()
                ftps.quit()
                message = f"FTPS connected successfully on attempt {attempt}"
                return True, message
            except Exception as exc:
                message = f"FTPS attempt {attempt} failed: {exc}"
                if attempt < max_retries:
                    # Comment below line if DEBUG logs are overwhelming
                    enable_debug = True
                    logger.warning(message)
                    time.sleep(delay)
            finally:
                if ftps:
                    # noinspection PyBroadException
                    try:
                        ftps.set_debuglevel(0)
                    except Exception:
                        pass
                    # noinspection PyBroadException
                    try:
                        ftps.close()
                    except Exception:
                        pass

        return False, message
