import logging
import os
import traceback
from typing import Optional


def setup_logging(level: Optional[str] = None, logfile: Optional[str] = None) -> None:
    """Configure basic logging to console and optional file."""
    log_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    log_file = logfile or os.getenv("LOG_FILE", "debug.log")

    handlers = [logging.StreamHandler()]
    if log_file:
        try:
            handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
        except Exception:
            # Fallback to console-only if file handler fails
            pass

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
    )


def format_exception() -> str:
    """Return the current exception traceback as a string."""
    return traceback.format_exc()

