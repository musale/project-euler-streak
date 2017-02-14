#!/usr/bin/env python
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
GITHUB_URL = "https://+%s+:+%s+@github.com/+%s+/project-euler-streak.git" % (
    GITHUB_USERNAME, GITHUB_PASS, GITHUB_USERNAME,)


# 1. open the counter file and check current file counter
counter = open("counter.txt", "r")
counter_value = counter.readline()
counter_value = counter_value[:-1]


def main():
    """Starting point of execution."""
    if len(counter_value) == 0:
        # nothing has been written to counter.
        # will probably run just once
        # write to it 001
        commit_message = create_counter_commit("001")

        # now run the first euler problem into 001.py
        # it always asks for input in order to create file so
        # do it automatically by starting with yes and piping euler command
        os.system("yes|euler")

        # add the problem py file
        os.system("git add .")

        # commit the problem py file
        os.system("git commit -m '{0}'".format(commit_message,))

        # push it all upstream
        os.system("git push origin master")
    else:
        commit_message = create_counter_commit(counter_value)
        os.system("yes|euler {0}".format(counter_value))

        # add the problem py file
        os.system("git add .")

        # commit the problem py file
        os.system("git commit -m '{0}'".format(commit_message,))

        # push it all upstream
        os.system("git push origin master")


def create_counter_commit(count):
    """Create a counter write and commit message."""
    printer("writing counter file ...")
    counter = open("counter.txt", "w")
    counter.write(count)
    counter.close()

    # add the counter.txt file
    os.system("yes|git add -p counter.txt")

    # create commit for new problem file
    commit_message = "Euler Problem {0} file added\n - This is the first commit for the number {1} problem".format(
        count, count)

    # commit the counter.txt file
    os.system("git commit -m 'Set up problem {0}'".format(count,))
    return commit_message


def printer(message):
    print message

if __name__ == "__main__":
    main()
