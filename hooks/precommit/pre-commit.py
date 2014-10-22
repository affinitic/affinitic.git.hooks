#!/usr/bin/env python2.7
# inspired by http://tech.yipit.com/2011/11/16/183772396/
import os
import re
import subprocess
import sys

modified = re.compile('^(?:M|A)(\s+)(?P<name>.*)')

CHECKS = [
    {
        'output': 'python: Checking for pdbs...',
        'command': 'grep -n "import pdb" %s',
        'ignore_files': ['.*pre-commit'],
        'match_files': ['.*\.py$'],
        'print_filename': True,
    },
    {
        'output': 'python: Checking for ipdbs...',
        'command': 'grep -n "import ipdb" %s',
        'ignore_files': ['.*pre-commit'],
        'match_files': ['.*\.py$'],
        'print_filename': True,
    },
    {
        'output': 'python: Checking for pyflakes',
        'command': 'pyflakes %s',
        'match_files': ['.*\.py$'],
        'print_filename': True,
    },
    {
        'output': 'python: Checking for pep8',
        'command': 'pep8 --repeat --ignore E5 %s',
        'match_files': ['.*\.py$'],
        'print_filename': True,
    },
    {
        'output': 'python: Checking for print statements...',
        'command': 'grep -n \'print \' %s',
        'match_files': ['.*\.py$'],
        'ignore_files': ['.*migrations.*', '.*management/commands.*',
                         '.*manage.py', '.*/scripts/.*', '.*pre-commit.py'],
        'print_filename': True,
    },
    {
        'output': 'js: Checking for console.log()...',
        'command': 'grep -n console.log %s',
        'match_files': ['.*\.js$'],
        'print_filename': True,
    },
    {
        'output': 'puppet: Checking Puppet lint',
        'command': 'puppet-lint %s',
        'match_files': ['.*\.pp$'],
        'print_filename': True,
    },
]


def matches_file(file_name, match_files):
    return any(re.compile(match_file).match(file_name) for match_file in match_files)


def check_files(files, check, repo_root):
    result = 0
    print check['output']
    for file_name in files:
        if 'match_files' not in check or matches_file(file_name, check['match_files']):
            if 'ignore_files' not in check or not matches_file(file_name, check['ignore_files']):
                process = subprocess.Popen(check['command'] % (repo_root + '/' + file_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = process.communicate()
                if out or err:
                    if check['print_filename']:
                        prefix = '\t%s:' % file_name
                    else:
                        prefix = '\t'
                    output_lines = ['%s%s' % (prefix, line) for line in out.splitlines()]
                    print '\n'.join(output_lines)
                    if err:
                        print err
                    result = 1
    return result


def main(all_files):
    p = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                         stdout=subprocess.PIPE)
    out, _ = p.communicate()
    repo_root = out.splitlines()[0]
    files = []
    if all_files:
        for root, dirs, file_names in os.walk('.'):
            for file_name in file_names:
                files.append(os.path.join(root, file_name))
    else:
        p = subprocess.Popen(['git', 'status', '--porcelain'],
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            match = modified.match(line)
            if match:
                files.append(match.group('name'))
    result = 0
    for check in CHECKS:
        result = check_files(files, check, repo_root) or result
    sys.exit(result)


if __name__ == '__main__':
    all_files = False
    if len(sys.argv) > 1 and sys.argv[1] == '--all-files':
        all_files = True
    main(all_files)
