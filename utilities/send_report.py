from __future__ import annotations

import time, datetime, ssl, smtplib, mimetypes, json
from email.message import EmailMessage
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Import project config
from config.config import Config


# noinspection PyBroadException
class Report:
    # ---------- Legacy methods (start) ----------
    @classmethod
    def __build_message_summary(cls, json_path: str) -> str:
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"Report sending failed. JSON report not found: {json_path}")
        json_object = json.loads(path.read_text())
        test_result = None
        exit_status = int(json_object.get("exitcode", -1))  # Default to -1 if exitcode is missing
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
            f"Total: {summary_object.get('collected', 0)}<br/>"
            f"<span style='color:green;'>Passed: {summary_object.get('passed', 0)}</span><br/>"
            f"<span style='color:gold;'>Rerun: {summary_object.get('rerun', 0)}</span><br/>"
            f"<span style='color:red;'>Failed: {summary_object.get('failed', 0)}</span><br/>"
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
                            <p>Hello, Automated EFM environments login verification completed.</p>
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
    # ---------- Legacy methods (end) ----------

    @classmethod
    def __is_transient(cls, exception: Exception) -> bool:
        code = getattr(exception, "smtp_code", None)
        # Treat 4xx as transient; 5xx as permanent
        return isinstance(exception, smtplib.SMTPResponseException) and code and 400 <= code < 500

    # ---------- New extended methods (start) ----------
    @classmethod
    def __compute_counts(cls, parsed: dict) -> Tuple[int, int, int, int]:
        raw = parsed.get("raw", {})
        # Attempt to get the counts from top-level summary
        summary = raw.get("summary") or raw.get("metadata") or {}
        collected = summary.get("total") or None
        # collected = summary.get("collected") or summary.get("total") or None
        passed = summary.get("passed")
        failed = summary.get("failed")
        rerun = summary.get("rerun") or summary.get("reruns") or 0

        if collected is not None and (passed is not None or failed is not None):
            # Covert counts to int
            total = int(collected)
            passed = int(passed) if passed is not None else 0
            failed = int(failed) if failed is not None else 0
            rerun = int(rerun or 0)
            return total, passed, rerun, failed

        # Fallback: compute from tests list
        tests = parsed.get("tests", [])
        total = len(tests)
        passed = sum(1 for t in tests if (t.get("outcome") or "").lower() == "passed")
        failed = sum(1 for t in tests if (t.get("outcome") or "").lower() == "failed")
        # detect rerun attempts if available in test keys (flexible)
        rerun = sum(1
                    for t in tests
                    if str(t.get("rerun", "")).lower() in ("true", "1", "yes")
                    or "rerun" in (t.get("nodeid") or "").lower()
                    or (t.get("outcome") or "").lower() == "rerun")
        return total, passed, rerun, failed

    @classmethod
    def __parse_json(cls, json_path: str) -> Dict[str, Any]:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results: Dict[str, Dict[str, str]] = {}
        tests = data.get("tests", [])

        for test in tests:
            nodeid = test.get("nodeid", "")
            outcome = (test.get("outcome") or "").lower()

            # For safer side
            parts = nodeid.split(" - ")
            if len(parts) < 2:
                continue

            login_part = parts[0].strip()
            env_part = parts[1].strip()

            lp = login_part.lower()
            if "okta" in lp:
                login = "Okta"
            elif "external" in lp:
                login = "External user"
            elif "sftp" in lp and "password" in lp:
                login = "SFTP password"
            elif "sftp" in lp and ("ssh" in lp or "ssh key" in lp):
                login = "SFTP SSH key"
            elif "ftps" in lp:
                login = "FTPS password"
            else:
                login = login_part

            env = env_part.replace("env", "").strip().upper()
            results.setdefault(env, {})[login] = outcome

        return {"results": results, "tests": tests, "raw": data}

    @classmethod
    def __build_message_html(cls, json_path: str) -> str:
        DEFAULT_ENVS = ["DEV", "DEV-INT", "TEST", "STAGING"]
        DEFAULT_LOGINS = ["Okta", "External user", "SFTP password", "SFTP SSH key", "FTPS password"]
        envs: List[str] = DEFAULT_ENVS
        logins: List[str] = DEFAULT_LOGINS

        # Parse the json report
        parsed = Report.__parse_json(json_path)

        # Compute counts - total, passed, rerun, and failed
        total, passed, rerun, failed = Report.__compute_counts(parsed)

        # Build CSS for result table
        css = """
            table.summary {
                border-collapse: collapse;
                width: 100%;
                max-width: 900px;
                font-family: Arial, sans-serif;
                font-size: 13px;
            }
            table.summary th, table.summary td {
                border: 1px solid #dcdcdc; /* subtle light-gray border */
                padding: 8px 10px;
                text-align: center;
                vertical-align: middle;
            }
            table.summary th {
                background-color: #fafafa;
                font-weight: 700;
            }
            .pass { color: #067c06; font-weight: 700; }
            .fail { color: #c43b2b; font-weight: 700; }
            .other { color: #666; }
            .row-summary { font-size: 12px; color: #666; margin-top: 4px; }
            .top-summary { font-family: Arial, sans-serif; font-size: 14px; color: #333; margin-bottom: 8px; }
            """

        # Start building main HTML
        html = (f"<html><head><style>{css}</style></head><body>"
                "<u>Summary:</u><br/>")
        # Add top-level counts summary line
        html += (f'<div class="top-summary"><strong>Total:</strong> {total} &nbsp;|&nbsp; '
                 f'<span class="pass"><strong>Passed:</strong> {passed}</span> &nbsp;|&nbsp; '
                 f'<span class="other"><strong>Rerun:</strong> {rerun}</span> &nbsp;|&nbsp; '
                 f'<span class="fail"><strong>Failed:</strong> {failed}</span></div>')

        html += '<table class="summary" role="table" aria-label="Environment login summary">'
        # Build header
        html += "<tr><th>Env / Login</th>" + "".join(f"<th>{l}</th>" for l in logins) + "</tr>"

        results = parsed["results"]
        for env in envs:
            env_results = results.get(env, {})
            # Compute per-row counts: total checks present for this env, and how many passed
            available_checks = sum(1 for l in logins if l in env_results)
            passed_checks = sum(1 for l in logins if env_results.get(l) == "passed")
            # Row summary string like "4/5 Passed"
            row_summary = f"{passed_checks}/{available_checks} Passed" if available_checks > 0 else "—"

            html += "<tr>"
            # Env cell: show name and small row summary underneath
            html += ("<td>"
                     f"<div style='font-weight:700;'>{env}</div>"
                     f"<div class='row-summary'>{row_summary}</div>"
                     "</td>")
            # Other cells
            for login in logins:
                outcome = env_results.get(login, "")
                if outcome == "passed":
                    cell = '<span class="pass">✓ Passed</span>'
                elif outcome == "failed":
                    cell = '<span class="fail">✗ Failed</span>'
                elif outcome:
                    cell = f'<span class="other">{outcome}</span>'
                else:
                    cell = '<span class="other">—</span>'
                html += f"<td>{cell}</td>"

            html += "</tr>"

        html += ("</table>"
                 "<p>Please find the test report attached.</p>"
                 "<p>Regards,<br/>Tejas<br/>Python selenium pytest automation</p>"
                 "</body></html>")
        return html

    @classmethod
    def __build_message_extended(cls,
                                 recipients: List[str],
                                 subject_prefix: str,
                                 report_html_path: str,
                                 report_json_path: str) -> EmailMessage:
        html = Report.__build_message_html(report_json_path)

        message = EmailMessage()
        message["Subject"] = f"{subject_prefix} - {datetime.date.today().strftime('%m/%d/%Y')}"
        message["From"] = Config.send_report_email
        message["To"] = ", ".join(recipients)
        message.set_content("Please find the HTML report attached.")
        message.add_alternative(html, subtype="html")

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
    # ---------- New extended methods (end) ----------

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

        # Legacy method call - build basic message
        """
        message = Report.__build_message(recipients,
                                         subject_prefix,
                                         relative_report_html_path,
                                         relative_report_json_path)
        """

        # New method call - build extended message
        message = Report.__build_message_extended(recipients,
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
