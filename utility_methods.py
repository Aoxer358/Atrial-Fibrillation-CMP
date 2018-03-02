import os


def create_dir(dir_name):
    if not os.path.exists('data/{}'.format(dir_name)):
        os.makedirs('data/{}'.format(dir_name))


def average(list):
    return int(sum(list) / len(list))


def arr_direction(arr):
    if arr[0] == 0 and arr[1] == 0:
        return 0
    elif arr[0] == 0 and arr[1] > 0:
        return 1
    elif arr[0] > 0 and arr[1] > 0:
        return 2
    elif arr[0] > 0 and arr[1] == 0:
        return 3
    elif arr[0] > 0 and arr[1] < 0:
        return 4
    elif arr[0] == 0 and arr[1] < 0:
        return 5
    elif arr[0] < 0 and arr[1] < 0:
        return 6
    elif arr[0] < 0 and arr[1] == 0:
        return 7
    else:
        return 8


def count_consecutive(list, start):
    count = 0
    if list[start] == 0:
        start += 1
        count += 1

    for i in range(start + 1, len(list)):
        if list[i] == 0 or list[i] == list[start]:
            count += 1
        else:
            return count

    return count


def count_max_consecutive(list):
    max_count = 0
    for i in range(len(list)):
        max_count = max(count_consecutive(list, i), max_count)

    return max_count
