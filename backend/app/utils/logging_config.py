import logging
import sys


def configure_logging() -> None:
    """Configure a simple, readable logging format for the whole app."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
    # Keep uvicorn's own loggers, just make sure our format applies everywhere.
    for noisy_logger in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(noisy_logger).setLevel(logging.INFO)
