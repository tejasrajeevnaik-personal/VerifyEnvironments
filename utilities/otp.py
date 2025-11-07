import re
import time
import imaplib
import email
import logging
from typing import Optional


# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# If a logger handler is not already attached
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class OTP:
    @staticmethod
    def get_otp_from_gmail_imap(gmail_address: str,
                                gmail_app_password: str,
                                subject_filter: str = "",
                                timeout: int = 120,
                                poll_interval: float = 2.0,
                                mark_all_read: bool = True) -> Optional[str]:
        # Wait for OTP to arrive
        time.sleep(30)

        otp_pattern = re.compile(r"\b\d{6}\b")
        end_time = time.time() + timeout
        M = None
        logger.info("Connecting to Gmail IMAP for %s", gmail_address)

        try:
            M = imaplib.IMAP4_SSL("imap.gmail.com")
            M.login(gmail_address, gmail_app_password)
            M.select("INBOX")
            logger.debug("Successfully logged into Gmail IMAP.")

            search_criteria = '(UNSEEN)'
            if subject_filter:
                search_criteria = f'(UNSEEN SUBJECT "{subject_filter}")'
            logger.debug("Search criteria: %s", search_criteria)

            while time.time() < end_time:
                try:
                    typ, data = M.search(None, search_criteria)
                    if typ != 'OK':
                        logger.warning("IMAP search failed: %s", typ)
                        time.sleep(poll_interval)
                        continue

                    uids = data[0].split()
                    logger.debug("Found %d unseen emails.", len(uids))
                    for uid in reversed(uids):
                        typ, msg_data = M.fetch(uid, "(RFC822)")
                        if typ != 'OK' or not msg_data:
                            logger.warning("Fetch failed for UID %s", uid)
                            continue

                        raw = msg_data[0][1]
                        if not raw:
                            continue
                        msg = email.message_from_bytes(raw)
                        subject = msg.get("Subject", "") or ""
                        logger.debug("Processing email: subject='%s'", subject)

                        if subject_filter and subject_filter.lower() not in subject.lower():
                            logger.debug("Subject filter '%s' not in '%s'", subject_filter, subject)
                            continue

                        # Collect body text
                        body_parts = []
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            if ctype in ("text/plain", "text/html"):
                                try:
                                    payload = part.get_payload(decode=True)
                                    if not payload:
                                        continue
                                    charset = part.get_content_charset() or "utf-8"
                                    text = payload.decode(charset, errors="ignore")
                                    body_parts.append(text)
                                except Exception as e:
                                    logger.exception("Failed to decode part: %s", e)

                        body = "\n".join(body_parts)
                        if not body:
                            logger.debug("No readable body content found for UID %s", uid)
                            continue

                        m = otp_pattern.search(body)
                        if m:
                            otp = m.group()
                            logger.info("OTP found: %s", otp)
                            return otp

                    logger.debug("No OTP found yet, waiting %.1f seconds...", poll_interval)
                    time.sleep(poll_interval)

                except imaplib.IMAP4.abort:
                    logger.warning("IMAP connection aborted, reconnecting ...")
                    try:
                        time.sleep(1)
                        M = imaplib.IMAP4_SSL("imap.gmail.com")
                        M.login(gmail_address, gmail_app_password)
                        M.select("INBOX")
                        logger.debug("Reconnected to IMAP successfully.")
                    except Exception as e:
                        logger.error("Reconnection failed: %s", e)
                        time.sleep(poll_interval)
                except Exception as e:
                    logger.exception("Unexpected error during polling: %s", e)
                    time.sleep(poll_interval)

            logger.warning("Timed out after %d seconds waiting for OTP.", timeout)
            return None

        finally:
            if M is not None:
                if mark_all_read:
                    try:
                        M.store("1:*", '+FLAGS', '\\Seen')
                        logger.info("All emails marked as read.")
                    except Exception as e:
                        logger.warning("Could not mark emails as read: %s", e)
                # noinspection PyBroadException
                try:
                    M.close()
                except Exception:
                    pass
                # noinspection PyBroadException
                try:
                    M.logout()
                except Exception:
                    pass
                logger.debug("IMAP connection closed and logged out.")