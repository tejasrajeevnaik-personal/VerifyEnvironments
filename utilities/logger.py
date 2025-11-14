import logging
import sys
from typing import Optional

DEFAULT_FORMATTER = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEFAULT_LEVEL = logging.INFO


def setup_logger(level: Optional[int] = None,
                 formatter: Optional[str] = None,
                 force: bool = False) -> None:
    level = level if level is not None else DEFAULT_LEVEL
    formatter = formatter if formatter is not None else DEFAULT_FORMATTER

    root = logging.getLogger()
    if root.handlers:
        if not force:
            # Do not re-configure just return
            return
        # Force reconfigure: remove existing handlers
        for h in list(root.handlers):
            root.removeHandler(h)
            # noinspection PyBroadException
            try:
                h.close()
            except Exception:
                pass

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(formatter))
    root.setLevel(level)
    root.addHandler(handler)

    # 1. Route warnings through logger
    logging.captureWarnings(True)

    # 2. Route uncaught exceptions through logger
    def _excepthook(exc_type, exc, tb):
        logging.getLogger("uncaught").exception("Uncaught exception", exc_info=(exc_type, exc, tb))

    sys.excepthook = _excepthook


def teardown_logger() -> None:
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        # noinspection PyBroadException
        try:
            h.close()
        except Exception:
            pass
    logging.shutdown()
    # Restore default excepthook
    sys.excepthook = sys.__excepthook__


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or __name__)
