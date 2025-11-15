import os, re, base64, tempfile
from datetime import datetime
import pytest

# Import project logger
from utilities.logger import setup_logger, teardown_logger

RUN_TS = datetime.now().strftime("%Y%m%d_%H%M%S")


def pytest_configure(config):
    setup_logger()


# Optional: This is to teardown the custom logger and restore sys logger at the end of pytest run
"""
def pytest_unconfigure(config):
    teardown_logger()
"""


# Get values from custom test name decorator - display_name
def pytest_collection_modifyitems(items):
    for item in items:
        mark = item.get_closest_marker("display_name")
        if mark:
            item._nodeid = mark.args[0]


# ---------- Pytest-html screenshot capture method and its utility methods ----------
def _safe_name(nodeid: str) -> str:
    return re.sub(r"[^\w\-.]+", "", nodeid).strip("_")


def _extract_driver(fixture_object):
    # Is driver directly present as root object?
    if hasattr(fixture_object, "save_screenshot"):
        return fixture_object
    # Is driver present at root - 1? like login.driver
    driver = getattr(fixture_object, "driver", None)
    if driver and hasattr(driver, "save_screenshot"):
        return driver
    return None


def _find_driver_from_item(item):
    # Look through all fixture objects bound to this test
    for fixture_object in item.funcargs.values():
        driver = _extract_driver(fixture_object)
        if driver:
            return driver
    return None


# Method to capture screenshots for failed UI tests and embed them in pytest-html report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Capture screenshot only on failure in phases - setup, call, or teardown
    if report.passed or report.when not in ("setup", "call", "teardown"):
        return

    driver = _find_driver_from_item(item)
    if not driver:
        return

    temp_path = tempfile.mkdtemp(f"Screenshots_{RUN_TS}")
    fname = os.path.join(temp_path, f"{_safe_name(item.nodeid)}_{report.when}_{RUN_TS}.png")

    # Save and embed screenshot
    driver.save_screenshot(fname)
    b64 = base64.b64encode(driver.get_screenshot_as_png()).decode("utf-8")
    html = item.config.pluginmanager.getplugin("html")
    if html:
        extra = getattr(report, "extra", [])
        extra.append(html.extras.image(b64, mime_type="image/png", extension="png"))
        extra.append(html.extras.html(f'<div>Saved: <code>{fname}</code></div>'))
        report.extra = extra
