#!/usr/bin/env python
"""Run file to execute the eauler streak maker."""
import json
import os
from os.path import dirname, join

import dotenv
import requests

# load the environment variables
dotenv_path = join(dirname("__file__"), '.env')
dotenv.read_dotenv(dotenv_path)
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

counter_value = open("counter.txt", "r").readline()

# POST /repos/:owner/:repo/git/commits
COMMIT_URL = "https://api.github.com/repos/{0}/{1}/git/commits".format(
    GITHUB_USERNAME, GITHUB_REPO)

MASTER = "https://api.github.com/repos/{0}/{1}/git/refs/heads/master".format(
    GITHUB_USERNAME, GITHUB_REPO)
TREES = "https://api.github.com/repos/{0}/{1}/git/trees".format(
    GITHUB_USERNAME, GITHUB_REPO)


def get_head():
    """Get the sha of the master branch."""
    response = requests.get(MASTER)
    last_commit_sha = json.loads(response.content)['object']['sha']
    print last_commit_sha
    return last_commit_sha


def get_last_commit(LAST_COMMIT_URL):
    """Get the last commit."""
    response = requests.get(LAST_COMMIT_URL)
    last_tree_sha = json.loads(response.content)['tree']['sha']
    return last_tree_sha


def create_tree_obj(base_tree, path):
    """Create tree object (also implicitly creates a blob based on content)."""
    payload = {
        "base_tree": base_tree,
        "tree": [
            {
                "path": path,
                "mode": "100644",
                "type": "blob",
            }
        ]
    }
    response = requests.post(TREES, json=payload)
    new_content_tree_sha = json.loads(response.content)['sha']
    return new_content_tree_sha


def create_commit(last_commit_sha, new_content_tree_sha, message):
    """Create a new commit and POSTS to the COMMIT_URL."""
    payload = {
        "parents": [last_commit_sha],
        "tree": new_content_tree_sha,
        "message": message
    }
    print payload
    response = requests.post(COMMIT_URL, json=payload)
    print json.loads(response.content)
    new_commit_sha = json.loads(response.content)['sha']
    return new_commit_sha


def update_branch(new_commit_sha):
    """Update the branch with new commit."""
    payload = {
        "ref": "refs/heads/master",
        "sha": new_commit_sha
    }
    response = requests.patch(COMMIT_URL, json=payload)
    return response.status


def main():
    """Starting point of execution."""
    # get the head of the master branch
    last_commit_sha = get_head()
    LAST_COMMIT = "https://api.github.com/repos/{0}/{1}/git/commits/{2}".format(
        GITHUB_USERNAME, GITHUB_REPO, last_commit_sha)
    # get the last commit
    last_tree_sha = get_last_commit(LAST_COMMIT)

    if len(counter_value) == 0:
        # nothing has been written to counter.
        # will probably run just once
        # write to it 001
        create_counter_commit("001", last_commit_sha, last_tree_sha)
    else:
        create_counter_commit(counter_value, last_commit_sha, last_tree_sha)


def create_counter_commit(count, last_commit_sha, last_tree_sha):
    """Create a counter write and commit message."""
    counter = open("counter.txt", "w")
    counter.write(count)
    counter.close()
    commit_message = "Set up new problem {0}".format(count,)
    new_content_tree_sha = create_tree_obj(last_tree_sha, "counter.txt")

    new_commit_sha = create_commit(
        last_commit_sha, new_content_tree_sha, commit_message)
    update_branch(new_commit_sha)

    # now run the first euler problem into 001.py
    # it always asks for input in order to create file so
    # do it automatically by starting with yes and piping euler command
    if count.count('0') == 1:
        new_count = "00{0}".format(str(int(count) + 1))
    if count.count('0') >= 2:
        new_count = "0{0}".format(str(int(count) + 1))

    # get new values
    last_commit_sha = get_head()
    LAST_COMMIT = "https://api.github.com/repos/{0}/{1}/commits/#{2}".format(
        GITHUB_USERNAME, GITHUB_REPO, last_commit_sha)
    # get the last commit
    last_tree_sha = get_last_commit(LAST_COMMIT)
    print "LAST COMMIT"
    print last_tree_sha
    if count == '001':
        os.system("yes|euler")
        create_problem_file_commit(new_count, last_commit_sha, last_tree_sha)
    else:
        os.system("yes|euler {0}".format(new_count))
        create_problem_file_commit(new_count, last_commit_sha, last_tree_sha)


def create_problem_file_commit(count, last_commit_sha, last_tree_sha):
    """Create a commit for the problem file."""
    # create commit for new problem file
    commit_message = "Euler Problem {0} file added\n - This is the first commit for the number {1} problem".format(
        count, count)
    new_content_tree_sha = create_tree_obj(
        last_tree_sha, "{0}.py".format(count))

    new_commit_sha = create_commit(
        last_commit_sha, new_content_tree_sha, commit_message)
    status = update_branch(new_commit_sha)
    print status
    print "DONE"
    return status


if __name__ == "__main__":
    main()
