import time


def get_day():
    time_data = time.localtime(time.time())
    return f'{time_data.tm_mday}-{time_data.tm_mon}-{time_data.tm_year}'


if __name__ in '__main__':
    print(get_day())
