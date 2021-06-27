from junitparser import JUnitXml, Error, Failure, Skipped
from github import GitHub
import os
import hashlib

def get_failures(filepath):
    xml = JUnitXml.fromfile(filepath)

    failures = []

    for suite in xml:
        for case in suite:
            if len(case.result) > 0:
                if type(case.result[0]) is Failure:
                    failures.append((case.name, case.result[0]))

    for f in failures:
        create_issue(f)

def hash_func(string):
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()  

def create_issue(f):
    git = GitHub(os.environ['INPUT_TOKEN'])

    # GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
    repo = git.fetch_repository(os.environ['GITHUB_REPOSITORY'])

    body = 'There was a failed test in {}. This is the following error message: {}'.format(f[0], f[1])

    issue = repo.create_issue(
        title=f[0] + '::' + hash_func(f[1].message),
        body=body
    )

get_failures(os.environ['INPUT_FILE'])