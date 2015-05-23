from .tag_getters import (
    git_tag_getter,
    hg_tag_getter
)


__all__ = ['REPO_TAG_GETTERS']


REPO_TAG_GETTERS = {
    'git': git_tag_getter,
    'hg': hg_tag_getter
}

