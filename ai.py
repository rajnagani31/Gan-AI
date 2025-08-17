import logging

# Configure logger to show in console
logging.basicConfig(
    level=logging.ERROR,  # Only show ERROR and above
    format="%(levelname)s: %(message)s"
)
try:
    x = 10 / 0
except Exception as e:
    logging.error("An error occurred: %s", e)