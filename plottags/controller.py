import argparse
import os
import sys

from .constants import REPO_TAG_GETTERS
from .models import Tag
from .views import view_tags


def get_repo_type():
    cwd = os.getcwd() 
    is_repo_type = lambda repo_type: os.path.exists(os.path.join(cwd, '.' + repo_type))
    for repo_type in REPO_TAG_GETTERS.keys():
        if is_repo_type(repo_type):
            return repo_type
    return None


def get_tag_tuples(repo_type):
    tag_getter = REPO_TAG_GETTERS[repo_type]
    return tag_getter()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='increase output verbosity', 
                        action='store_true')
    parser.add_argument('-f', '--file', help='file to save plot to.')
    args = parser.parse_args()
     
    repo_type = get_repo_type()
    if not repo_type:
        if args.verbose:
            print('Current working directory is not a repository')
        sys.exit(1)

    if args.verbose: 
        print('Gathering information for {} repo'.format(repo_type))
    tag_tuples = get_tag_tuples(repo_type)

    tags = [Tag(tag_tuple) for tag_tuple in tag_tuples]
    view_tags(tags, file_name=args.file)

