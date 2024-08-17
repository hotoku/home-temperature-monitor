import base64
import hashlib
import hmac
import json
import time
import uuid
from pprint import pprint

import certifi
import click
import urllib3
from pydantic import BaseModel

from .update import update


@click.group()
def main():
    pass


if __name__ == "__main__":
    main.add_command(update)
    main()
