import click
from app import TimeLoggerApp
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@click.command()
@click.option('--preset', type=click.Choice(['weekly', 'monthly']), help='Use a predefined configuration preset')
def main(preset: str | None) -> None:
    """Time Tracker CLI for logging time to Zoho."""
    logger.info("Starting Time Tracker application")
    app = TimeLoggerApp()

    if preset:
        logger.info(f"Using preset: {preset}")
        app.run(preset=preset)
    else:
        logger.info("Using default configuration from config.ini")
        app.run()

    logger.info("Time logging process completed")


if __name__ == "__main__":
    main()