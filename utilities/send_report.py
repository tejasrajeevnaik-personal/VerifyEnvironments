from __future__ import annotations

import time, datetime, ssl, smtplib, mimetypes, json
from email.message import EmailMessage
from pathlib import Path
from typing import List

# Import project config
from config.config import Config


# noinspection PyBroadException
class Report:
    @classmethod
    def __is_transient(cls, exception: Exception) -> bool:
        code = getattr(exception, "smtp_code", None)
        # Treat 4xx as transient; 5xx as permanent
        return isinstance(exception, smtplib.SMTPResponseException) and code and 400 <= code < 500

    @classmethod
    def __build_message_summary(cls, json_path: str) -> str:
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"Report sending failed. JSON report not found: {json_path}")
        json_object = json.loads(path.read_text())
        test_result = None
        exit_status = int(json_object.get("exitcode", -1))  # default to -1 if missing
        match exit_status:
            case 0:
                test_result = "Passed"
            case 1:
                test_result = "Failed"
            case 2:
                test_result = "Execution interrupted"
            case 5:
                test_result = "No tests were collected"
            case _:
                test_result = "Unexpected error"
        summary_object = json_object.get("summary", {})
        summary = (
            f"Collected: {summary_object.get('collected', 0)}<br/>"
            f"<span style='color:green;'>Passed:</span> {summary_object.get('passed', 0)}<br/>"
            f"<span style='color:red;'>Failed:</span> {summary_object.get('failed', 0)}<br/>"
            f"Skipped: {summary_object.get('skipped', 0)}<br/>"
            f"<b>Overall status:</b> {test_result}"
        )
        return summary

    @classmethod
    def __build_message(cls,
                        recipients: List[str],
                        subject_prefix: str,
                        report_html_path: str,
                        report_json_path: str) -> EmailMessage:
        summary = Report.__build_message_summary(report_json_path)

        message = EmailMessage()
        message["Subject"] = f"{subject_prefix} - {datetime.date.today().strftime('%m/%d/%Y')}"
        message["From"] = Config.send_report_email
        message["To"] = ", ".join(recipients)
        message.set_content("Please find the HTML report attached.")
        message.add_alternative(f"""
                        <html>
                          <body>
                            <p>Hello,</p>
                            <p>Automated EFM environments login verification completed.</p>
                            <p>{summary}</p>
                            <p>Please find the HTML report attached.</p>
                            <p>Regards,<br/>Tejas<br/>Python selenium pytest automation</p>
                          </body>
                        </html>
                        """, subtype="html")

        html_path = Path(report_html_path)
        if not html_path.exists():
            raise FileNotFoundError(f"Report sending failed. HTML report not found: {html_path}")
        data = html_path.read_bytes()
        ctype, _ = mimetypes.guess_type(html_path.as_posix())
        if not ctype:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        message.add_attachment(data, maintype=maintype, subtype=subtype, filename=html_path.name)

        return message

    @staticmethod
    def send_report(recipients: List[str],
                    subject_prefix: str,
                    relative_report_html_path: str = "reports/report.html",
                    relative_report_json_path: str = "reports/report.json") -> None:
        TIMEOUT_S = 30
        MAX_RETRIES = 3
        BACKOFF_BASE = 2
        email = Config.send_report_email
        email_app_password = Config.send_report_email_app_password
        message = Report.__build_message(recipients,
                                         subject_prefix,
                                         relative_report_html_path,
                                         relative_report_json_path)

        context = ssl.create_default_context()
        attempt = 0
        while True:
            attempt += 1
            smtp = None
            try:
                smtp = smtplib.SMTP_SSL(Config.send_report_smtp_host,
                                        Config.send_report_smtp_port,
                                        timeout=TIMEOUT_S,
                                        context=context)
                smtp.ehlo()
                smtp.login(email, email_app_password)
                smtp.send_message(message)
                print(f"Report sent to: {", ".join(recipients)}")
                # Explicit graceful shutdown
                try:
                    smtp.quit()
                finally:
                    smtp.close()
                return
            except Exception as e:
                exception = e
                # Cleanup current connection
                try:
                    if smtp is not None:
                        smtp.close()
                except Exception:
                    pass

            if attempt <= MAX_RETRIES and Report.__is_transient(exception):
                time.sleep(BACKOFF_BASE ** attempt)  # 2s, 4s, 8s ...
                continue
            raise Exception(f"Send report failed. Local report path: {relative_report_html_path}")


if __name__ == "__main__":
    Report.send_report(Config.send_report_recipients,
                       Config.send_report_subject_prefix,
                       "reports/report.html",
                       "reports/report.json")
