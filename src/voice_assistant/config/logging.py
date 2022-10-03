import logging


def configure_logger() -> None:
    """Basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    )
