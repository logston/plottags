import argparse
from collections import defaultdict
import os
import pickle
import sys

from plottags import __version__
from .constants import REPO_TAG_INFO_GETTERS
from .models import Tag
from .views import view_tags


CWD = os.getcwd() 
CACHED_RESULTS_FILENAME = '.plottags_parse_results-{}.tmp'.format(__version__)


def path_exists(basename):
    return os.path.exists(os.path.join(CWD, basename))


def get_repo_type():
    for repo_type in REPO_TAG_INFO_GETTERS.keys():
        if path_exists('.' + repo_type):
            return repo_type
    return None


def get_tags_and_info(repo_type):
    tag_info_getter = REPO_TAG_INFO_GETTERS[repo_type]
    yield from tag_info_getter()


def extend_tag_tuples(tags):
    # make all tag tuples equal length
    max_len = max(len(t.tag_tuple) for t in tags)
    for tag in tags:
        len_diff = max_len - len(tag.tag_tuple)
        if len_diff:
            tag.tag_tuple = tag.tag_tuple + tuple(0 for _ in range(len_diff)) 
    return tags


def value_tags(tags):
    weights = [1 / i**2 for i in range(1, 10)]
    tags.sort(key=lambda t: t.tag_tuple) 

    value = 0
    tuple_length = len(tags[0].tag_tuple)
    previous_tag_tuple = tuple(0 for _ in range(tuple_length))
    for tag in tags:
        diff_index = 0
        for i in range(tuple_length):
            if tag.tag_tuple[i] != previous_tag_tuple[i]:
                diff_index = i
                break
        value += weights[diff_index]
        tag.value = value
        previous_tag_tuple = tag.tag_tuple

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quiet', help='decrease output verbosity', 
                        action='store_true')
    parser.add_argument('-f', '--file', help='file to save plot to.')
    parser.add_argument('--nocache', help="don't cache parsing results", 
                        action='store_true')
    args = parser.parse_args()

    tags = []
    if path_exists(CACHED_RESULTS_FILENAME):
        with open(CACHED_RESULTS_FILENAME, 'rb') as fd:
            tags = pickle.load(fd)
     
    if not tags or args.nocache: 
        repo_type = get_repo_type()
        if not repo_type:
            print('Current working directory is not a repository.')
            sys.exit(1)
    
        if not args.quiet:
            print('Gathering information for {} repo'.format(repo_type))
        tags_and_info = get_tags_and_info(repo_type)
        tags = [Tag(tag_info) for tag_info in tags_and_info]
        tags = [t for t in tags if t.tag_tuple]  # Drop tags with no tuple
        if not tags:
            print('This repo has no associated tags.')
            sys.exit(1)
        tags = extend_tag_tuples(tags)
        if not args.nocache:
            with open(CACHED_RESULTS_FILENAME, 'wb') as fd:
                pickle.dump(tags, fd, pickle.HIGHEST_PROTOCOL)

    if not args.quiet:
        print('Value tags')
    value_tags(tags)
     
    if not args.quiet:
        print('Building plot')
    view_tags(tags, file_name=args.file)

