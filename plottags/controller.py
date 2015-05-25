import argparse
from collections import defaultdict
import os
import pickle
import sys

from .constants import REPO_TAG_INFO_GETTERS
from .models import Tag
from .views import view_tags


CWD = os.getcwd() 
CACHED_RESULTS_FILENAME = '.plottags_parse_results.tmp'


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
    return tags, max_len


def value_tag_tuples(tags, tag_tuple_length):
    """
    Get a tuple of values that represent the relative version 
    values for each version type; major, minor, micro.
    """
    for index in range(tag_tuple_length):
        if index == 0:
            for tag in tags:
                tag.value_tuple = (tag.tag_tuple[0],)
        else: 
            version_groups = defaultdict(set)
            group_max = {}
            for tag in tags:
                version_groups[tag.tag_tuple[:index]].add(tag.tag_tuple[index])
            # find max of each group
            for version, set_ in version_groups.items():
                group_max[version] = max(set_)
            # update value tuple with new version value
            for tag in tags:
                denom = group_max[tag.tag_tuple[:index]] 
                value = tag.tag_tuple[index] / denom if denom else 0                 
                tag.value_tuple += (value,)


def value_tags(tags):
    weights = [1, 0.5, 0.1]
    for tag in tags:
        tag.value = sum(map(lambda x: x[0] * x[1], zip(tag.value_tuple, weights)))

    # Offset value of tag by value of previous versions. 
    # Drop support of offsets
    #values_by_major_version = defaultdict(set)
    #for tag in tags:
    #    values_by_major_version[tag.tag_tuple[0]].add(tag.value)
    #max_value_by_major_version = {k: max(v) for k, v in values_by_major_version.items()}
    #major_versions = max_value_by_major_version.keys()
    #for i, version in enumerate(sorted(major_versions)):
    #    # Continue if there is no prior max value
    #    if i == 0:
    #        continue
    #    prior_max_value = max_value_by_major_version[version - 1]
    #    for tag in tags:
    #        if tag.tag_tuple[0] == version:
    #            tag.value += prior_max_value


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
        tags, length = extend_tag_tuples(tags)
        if not args.quiet:
            print('Value tags')
        value_tag_tuples(tags, length)
        value_tags(tags)
        if not args.nocache:
            with open(CACHED_RESULTS_FILENAME, 'wb') as fd:
                pickle.dump(tags, fd, pickle.HIGHEST_PROTOCOL)
     
    if not args.quiet:
        print('Building plot')
    view_tags(tags, file_name=args.file)

