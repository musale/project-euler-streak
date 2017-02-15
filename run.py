#!/usr/bin/env python
"""Run file to execute the eauler streak maker."""
import json
import os
import time
from os.path import dirname, join

import dotenv
import requests

# load the environment variables
dotenv_path = join(dirname("__file__"), '.env')
dotenv.read_dotenv(dotenv_path)
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    'Authorization': 'token {0}'.format(GITHUB_TOKEN)
}

counter_value = open("counter.txt", "r").readline()
print "Counter at {0}".format(counter_value)

# POST /repos/:owner/:repo/git/commits
COMMIT_URL = "https://api.github.com/repos/{0}/{1}/git/commits".format(
    GITHUB_USERNAME, GITHUB_REPO)

MASTER = "https://api.github.com/repos/{0}/{1}/git/refs/heads/master".format(
    GITHUB_USERNAME, GITHUB_REPO)
TREES = "https://api.github.com/repos/{0}/{1}/git/trees".format(
    GITHUB_USERNAME, GITHUB_REPO)


def get_head():
    """Get the sha of the master branch."""
    print "1. Getting last commit SHA"
    response = requests.get(MASTER)
    last_commit_sha = json.loads(response.content)['object']['sha']
    return last_commit_sha


def get_last_commit(LAST_COMMIT_URL):
    """Get the last commit."""
    print "2. Getting last tree SHA"
    response = requests.get(LAST_COMMIT_URL)
    last_tree_sha = json.loads(response.content)['tree']['sha']
    return last_tree_sha


def create_tree_obj(base_tree, path, content):
    """Create tree object (also implicitly creates a blob based on content)."""
    print "3. Creating a new tree object"
    payload = {
        "base_tree": base_tree,
        "tree": [
            {
                "path": path,
                "mode": "100644",
                "type": "blob",
                "content": content
            }
        ]
    }
    response = requests.post(TREES, json=payload, headers=HEADERS)
    new_content_tree_sha = json.loads(response.content)['sha']
    return new_content_tree_sha


def create_commit(last_commit_sha, new_content_tree_sha, message):
    """Create a new commit and POSTS to the COMMIT_URL."""
    print "4. Creating a new commit"
    payload = {
        "parents": [last_commit_sha],
        "tree": new_content_tree_sha,
        "message": message
    }
    response = requests.post(COMMIT_URL, json=payload, headers=HEADERS)
    new_commit_sha = json.loads(response.content)['sha']
    return new_commit_sha


def update_branch(new_commit_sha):
    """Update the branch with new commit."""
    print "5. Updating the branch"
    payload = {
        "ref": "refs/heads/master",
        "sha": new_commit_sha
    }
    response = requests.patch(MASTER, json=payload, headers=HEADERS)
    return response.status_code


def main():
    """Starting point of execution."""
    print "STARTING ..."
    # get the head of the master branch
    last_commit_sha = get_head()

    LAST_COMMIT = "https://api.github.com/repos/{0}/{1}/git/commits/{2}".format(
        GITHUB_USERNAME, GITHUB_REPO, last_commit_sha)
    # get the last commit
    last_tree_sha = get_last_commit(LAST_COMMIT)

    create_counter_commit(counter_value, last_commit_sha, last_tree_sha)


def create_counter_commit(current, last_commit_sha, last_tree_sha):
    """Create a counter write and commit message."""
    new_count = get_new_count(current)

    counter = open("counter.txt", "w")
    counter.write(new_count)
    counter.close()

    file_content = open("counter.txt", "r")
    content = file_content.read()

    commit_message = "Set up new problem {0}".format(current,)
    new_content_tree_sha = create_tree_obj(
        last_tree_sha, "counter.txt", content)

    new_commit_sha = create_commit(
        last_commit_sha, new_content_tree_sha, commit_message)
    update_branch(new_commit_sha)

    # now run the first euler problem into 001.py
    # it always asks for input in order to create file so
    # do it automatically by starting with yes and piping euler command
    # get new values

    # sleep like for a minute then start over
    time.sleep(10)
    print "Commit problem file"
    last_commit_sha = get_head()
    LAST_COMMIT = "https://api.github.com/repos/{0}/{1}/git/commits/{2}".format(
        GITHUB_USERNAME, GITHUB_REPO, last_commit_sha)
    # get the last commit
    last_tree_sha = get_last_commit(LAST_COMMIT)
    os.system("yes|euler {0}".format(current))
    create_problem_file_commit(current, last_commit_sha, last_tree_sha)


def create_problem_file_commit(current, last_commit_sha, last_tree_sha):
    """Create a commit for the problem file."""
    # create commit for new problem file
    commit_message = "Euler Problem {0} file added\n - This is the first commit for the number {1} problem".format(
        current, current)
    content = open("{0}.py".format(current), "r").read()
    new_content_tree_sha = create_tree_obj(
        last_tree_sha, "{0}.py".format(current), content)

    new_commit_sha = create_commit(
        last_commit_sha, new_content_tree_sha, commit_message)

    update_branch(new_commit_sha)
    cleanup_repo(current)


def get_new_count(current):
    """Get a new count."""
    if current.count('0') <= 1:
        new_count = "0{0}".format(str(int(current) + 1))
    if current.count('0') == 2:
        new_count = "00{0}".format(str(int(current) + 1))
    print "New count is {0}".format(new_count,)
    return new_count


def cleanup_repo(files):
    """Clean up. Remove the created py file and commit counter.txt file."""
    os.system("rm {0}.py".format(files))
    os.system("git add .")
    os.system("git commit -m 'clean up {0}'".format(files))
    print "DONE!"


if __name__ == "__main__":
    main()
