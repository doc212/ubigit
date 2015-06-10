#!/usr/bin/env python
import git
import logging
import sys
logging.basicConfig(level=logging.DEBUG)

logging.debug("argv: %s", sys.argv)

#config
trash="trash"

if len(sys.argv) < 2:
    print "specify branch to trash"
    sys.exit(1)

repo=git.Repo(".")
target=sys.argv[1]

target=repo.refs[target]

if not isinstance(target, git.refs.Head):
    print target.path,"is not a branch"
    sys.exit(1)
if not target.is_remote():
    print "trashing local branch not supported"
    sys.exit(1)
if not target.is_detached:
    print "cannot trash symbolic reference"
    sys.exit(1)

remote=repo.remotes[target.remote_name]
trash=remote.refs[trash]

def fetch(target):
    remote=target.repo.remotes[target.remote_name]
    refspec = "%s:%s"%(target.remote_head, target.path)
    logging.debug("fetch %s from %s", refspec, remote.name)
    remote.fetch(refspec)

fetch(target)
fetch(trash)
base=repo.merge_base(target, trash)
if len(base) > 0 and base[0] == target.commit:
    logging.debug("%s can be fast-forwarded to %s", target, trash)
else:
    c=git.Commit.create_from_tree(repo, trash.commit.tree, "Trashing %s"%target.remote_head, [trash.commit, target.commit])
    logging.debug("created new commit %s", c)
    repo.branches.debug.commit=c

    refspec="%s:%s"%(c, trash.remote_head)
    logging.debug("pushing %s to %s", refspec, remote)
    remote.push(refspec)

refspec=":%s"%target.remote_head
logging.debug("pushing %s to %s", refspec, remote)
remote.push(refspec)
