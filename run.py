"""Run file to execute the eauler streak maker."""
import os
from os.path import dirname, join

import dotenv
import requests

MAX_CHARS = 140

# load the environment variables
dotenv_path = join(dirname("__file__"), '.env')
dotenv.read_dotenv(dotenv_path)
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_PASS = os.environ.get("GITHUB_PASS")
GITHUB_URL = "https://+%s+:+%s+@github.com/+%s+/streak-maker.git" % (
    GITHUB_USERNAME, GITHUB_PASS, GITHUB_USERNAME,)
