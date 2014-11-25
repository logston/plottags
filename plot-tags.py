import csv
import datetime


def get_version_tuple(version_str, repo_name=None):
    if repo_name == 'python':
        version_str = version_str.lstrip('v')
       
        tup = tuple(map(int, version_str.split('.')))
        return tup
    return (version_str,)


def get_unix_ts(time_str, repo_type=None):
    unix_ts = time_str
    if repo_type == 'hg':
        pattern = "%a %b %d %H:%M:%S %Y %z"
        dt = datetime.datetime.strptime(time_str, pattern) 
        unix_ts = int(dt.timestamp())

    return unix_ts


def list_get(list_, index, default=None):
    try:
        return list_[index]
    except IndexError:
        return default

def calculate_version_value(version_tuple, min_max_list):
    version_value = 0
    len_min_max_list = len(min_max_list)
    for i in range(len_min_max_list):
        min_, max_ = min_max_list[i] 
        part = version_tuple[i]
        part_value = (part - min_) / (max_ - min_)
        part_value_coeff = 10 ** (len_min_max_list - i)
        version_value += part_value_coeff * part_value

    return version_value


def resize_version_tuple(version_tuple, min_max_list):
    part_list = []
    len_min_max_list = len(min_max_list)
    for i in range(len_min_max_list):
        min_, max_ = min_max_list[i] 
        part = list_get(version_tuple, i, min_)
        part_list.append(part)

    return tuple(part_list)


def convert_time_tag_version_tuples(time_tag_list, max_version_tuple_length): 
    min_max_list = [[0, 0] for _ in range(max_version_tuple_length)]
    
    # Get max and min for each version part (eg. major, minor, patch)
    for _, version_tuple, _ in time_tag_list:
        for i, version_part in enumerate(version_tuple):
            min_max = min_max_list[i]
            if version_part <  min_max[0]:
                min_max[0] = version_part
            if version_part > min_max[1]:
                min_max[1] = version_part
 
    for i, (unix_ts, version_tuple, version_str) in enumerate(time_tag_list):
        version_tuple = resize_version_tuple(version_tuple, min_max_list)
        version_value = calculate_version_value(version_tuple, min_max_list)
        time_tag_list[i] = (unix_ts, version_value, version_tuple,  version_str)


def generate_std_csv(file_name, repo_name=None, repo_type=None):
    with open(file_name) as fd:
        csv_reader = csv.reader(fd)
        time_tag_list = []
        max_version_tuple_length = 0
        for time_str, version_str in csv_reader:
            pre_release = False
            for letter in ('a', 'b', 'c'):
                if letter in version_str:
                    pre_release = True
            # Do not include alphas, betas, release candidates
            if pre_release:
                continue
                    
            unix_ts = get_unix_ts(time_str, repo_type)
            version_tuple = get_version_tuple(version_str, repo_name) 
            tuple_length = len(version_tuple)
            if tuple_length > max_version_tuple_length:
                max_version_tuple_length = tuple_length
            time_tag_list.append((unix_ts, version_tuple, version_str))

    convert_time_tag_version_tuples(time_tag_list, max_version_tuple_length)

    return time_tag_list

if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt

    file_name = sys.argv[1]
    repo_name = sys.argv[2] if len(sys.argv) > 2 else None 
    repo_type = sys.argv[3] if len(sys.argv) > 3 else None
    time_tag_list = generate_std_csv(file_name, repo_name, repo_type)

    for tup in sorted(time_tag_list):
        print (tup)
    
    point_list_by_version = {}
    for unix_ts, version_value, version_tuple, version_str in time_tag_list:
        major_version = version_tuple[0]
        if major_version not in point_list_by_version:
            point_list_by_version[major_version] = []
        point_list_by_version[major_version].append((unix_ts,
                                                     version_value,
                                                     version_str))

    fig = plt.figure(figsize=(10, 8), dpi=100)
    axes = fig.add_subplot(111)
    axes.set_xlabel('Commit Date')
    axes.set_ylabel('<- Decreasing        Version Number        Increasing ->')
    axes.get_yaxis().set_ticks([])

    COLORS = {0: 'b', 1: 'r', 2: 'm', 3: 'y'}

    for major_version, version_data in point_list_by_version.items():
        unix_ts_list = []
        version_value_list = []
        version_str_list = []
        for unix_ts, version_value, version_str in version_data:
            unix_ts_list.append(unix_ts)
            version_value_list.append(version_value)
            version_str_list.append(version_str)

        for i, unix_ts in enumerate(unix_ts_list):
            unix_ts_list[i] = datetime.datetime.utcfromtimestamp(unix_ts)
        
        axes.scatter(unix_ts_list, version_value_list, 
                     s=10, 
                     c=COLORS[major_version], 
                     label='Python ' + str(major_version))
        axes.annotate(version_str_list[0],
                      xy=(unix_ts_list[0], version_value_list[0]),
                      xytext=(60, 0),
                      textcoords='offset points',
                      ha='center',
                      va='bottom',
                      bbox=dict(boxstyle='round,pad=0.25', fc='yellow', alpha=0.5),
                      arrowprops=dict(arrowstyle='->', relpos=(0., 0.), connectionstyle='arc3,rad=0.1'))
    plt.legend(loc='upper left')
    plt.show()
