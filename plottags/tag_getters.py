import datetime
import re
import subprocess


HG_DATESTRING_PATTERN = "%a %b %d %H:%M:%S %Y %z"


def git_tag_getter():
    tags = subprocess.check_output(['git', 'tag']).decode('utf-8')
    tags = tags.split('\n')
    tags = [str(tag) for tag in tags if tag]
    for tag in tags:
        shas = subprocess.check_output(['git', 'rev-list', tag]).decode('utf-8')
        shas = shas.split('\n')
        sha = shas[0]
        clargs = ['git', 'rev-list', '--format=%ct', '--max-count=1', tag]
        output = subprocess.check_output(clargs).decode('utf-8')
        unix_ts = int(output.split('\n')[1])
        dt = datetime.datetime.utcfromtimestamp(unix_ts)
        yield tag, sha, dt


def hg_tag_getter():
    tag_lines = subprocess.check_output(['hg', 'tags']).decode('utf-8')
    tag_lines = tag_lines.split('\n')
    tags_changesets = [tag_line.split() for tag_line in tag_lines if tag_line]
    # Ensure that tag has at least one number
    tags_changesets = [(t, c) for t, c in tags_changesets if re.search('\d', t)]
    for tag, changeset in tags_changesets:
        output = subprocess.check_output(['hg', 'log', '-r', changeset]).decode('utf-8')
        date_str = ''
        for line in output.split('\n'):
            if line[0:5] == 'date:':
                date_str = ' '.join(line.split()[1:])
                break
        dt = datetime.datetime.strptime(date_str, HG_DATESTRING_PATTERN)
        yield tag, changeset, dt

