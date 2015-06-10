#!/usr/bin/env python
import git
import logging
import sys
logging.basicConfig(level=logging.DEBUG)

logging.debug("argv: %s", sys.argv)

repo=git.Repo(".")
