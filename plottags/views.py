import random

import matplotlib.pyplot as plt


color_by_version = {}


def colors(version):
    global color_by_version
    if version not in color_by_version:
        color_by_version[version] = (random.random(), random.random(), random.random())
    return color_by_version[version]


def view_tags(tags, file_name=None):
    fig = plt.figure(figsize=(10, 8), dpi=100)
    axes = fig.add_subplot(111)
    axes.set_xlabel('Commit date for commit associated with tag')
    axes.set_ylabel('<- Decreasing        Version Number        Increasing ->')
    axes.get_yaxis().set_ticks([])

    for major_version in set(tag.tag_tuple[0] for tag in tags):
        dates = []
        values = []
        for tag in tags:
            if tag.tag_tuple[0] == major_version:
                dates.append(tag.dt)
                values.append(tag.value)
        axes.scatter(dates, values, c=colors(major_version))
        axes.annotate('Version {}.x'.format(major_version),
                      xy=(dates[0], values[0]),
                      xytext=(60, 0),
                      textcoords='offset points',
                      ha='center',
                      va='bottom',
                      bbox=dict(boxstyle='round,pad=0.15', fc='yellow', alpha=0.5),
                      arrowprops=dict(arrowstyle='->', relpos=(0., 0.), connectionstyle='arc3,rad=0.1'))

    if file_name:
        plt.savefig(file_name)
    else:
        plt.show()

