Affinitic git hooks
===================

Add this repository as your git template directory::

 git config --global init.templatedir '<THIS REPO PATH>'

To set these hooks on an existing clone, got to the root of your existing repo::

 rm .git/hooks
 git init

To commit and ignore check::

 git commit --no-verify

Pre-commit:
-----------

 - python: avoid pdb
 - python: avoid ipdb
 - python: avoid pyflakes error
 - python: avoid pep8 error
 - python: avoid print statements
 - js: avoid js console log

Post-checkout:
--------------

 - remove pyc files from the repo when switching branch

Commit message:
---------------

 - reference one of our ticket
