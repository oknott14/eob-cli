from src.cli import cli

# from src.cli import extract_eob
from src.config import config

if __name__ == "__main__":
    config()
    cli()
    # extract_eob("./eobs/blue-shield-eob.pdf")
