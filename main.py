from junitparser import JUnitXml, Error, Failure, Skipped
import github
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
    git = github.Github(os.environ['INPUT_TOKEN'])

    # GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
    repo = git.get_repo(os.environ['GITHUB_REPOSITORY'])

    body = 'There was a failed test in {}. This is the following error message: {}'.format(f[0], f[1])

    title = f[0] + '::' + hash_func(f[1].message)

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title == title:
            return

    issue = repo.create_issue(
        title= title,
        body=body
    )

get_failures(os.environ['INPUT_FILE'])