import random
import string
from datetime import datetime

import pytest
import yaml

from checkers import checkout, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout("mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder1'], data['folder2']),
                    '')


@pytest.fixture()
def clear_folders():
    return checkout(
        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder1'], data['folder2']),
        '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout('cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'], filename,
                                                                                           data['bs']), ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout('cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ''):
        return None, None
    if not checkout(
            'cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'], subfoldername,
                                                                                      testfilename, data['bs']), ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def make_bad_arx():
    checkout('cd {}; 7z a {}/bad_arx -t{}'.format(data['folder_in'], data['folder_out'], data['type']), 'Everything '
                                                                                                        'is Ok')
    checkout('truncate -s 1 {}/bad_arx.{}'.format(data['folder_out'], data['type']), '')


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
    yield
    print('Finish: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout('cat /proc/loadavg')
    checkout('echo "time: {} count: {} size: {} load: {}">> stat.txt'.format(datetime.now().strftime('%H:%M:%S.%f'),
                                                                             data['count'], data['bs'], stat), '')
