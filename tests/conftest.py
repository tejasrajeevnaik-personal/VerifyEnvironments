import os, re, base64, pytest
import tempfile
from datetime import datetime

RUN_TS = datetime.now().strftime("%Y%m%d_%H%M%S")


# Custom test name decorator
def pytest_collection_modifyitems(items):
    for item in items:
        mark = item.get_closest_marker("display_name")
        if mark:
            item._nodeid = mark.args[0]


def _safe_name(nodeid: str) -> str:
    return re.sub(r"[^\w\-.]+", "", nodeid).strip("_")


def _extract_driver(fixture_object):
    # is driver directly present as root object?
    if hasattr(fixture_object, "save_screenshot"):
        return fixture_object
    # is driver present at root - 1? like login.driver
    driver = getattr(fixture_object, "driver", None)
    if driver and hasattr(driver, "save_screenshot"):
        return driver
    return None


def _find_driver_from_item(item):
    # look through all fixture objects bound to this test
    for fixture_object in item.funcargs.values():
        driver = _extract_driver(fixture_object)
        if driver:
            return driver
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # if outcome is passed or failed not in setup, call, or teardown then return (don't take screenshot)
    # take screenshot only on failure in phase setup, call, or teardown
    if report.passed or report.when not in ("setup", "call", "teardown"):
        return

    driver = _find_driver_from_item(item)
    if not driver:
        return

    temp_path = tempfile.mkdtemp(f"Screenshots_{RUN_TS}")
    fname = os.path.join(temp_path, f"{_safe_name(item.nodeid)}_{report.when}_{RUN_TS}.png")

    # save + embed screenshot (pytest-html)
    driver.save_screenshot(fname)
    b64 = base64.b64encode(driver.get_screenshot_as_png()).decode("utf-8")

    html = item.config.pluginmanager.getplugin("html")
    if html:
        extra = getattr(report, "extra", [])
        extra.append(html.extras.image(b64, mime_type="image/png", extension="png"))
        extra.append(html.extras.html(f'<div>Saved: <code>{fname}</code></div>'))
        report.extra = extra
