import random
import string
from datetime import datetime

import pytest
import yaml

from checkers import ssh_checkout, ssh_get
from files import upload_files, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout('0.0.0.0', 'user2', '1111',
                        "mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder1'],
                                                   data['folder2']),
                        '')


@pytest.fixture()
def clear_folders():
    return ssh_checkout('0.0.0.0', 'user2', '1111',
                        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder1'],
                                                            data['folder2']),
                        '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout('0.0.0.0', 'user2', '1111',
                        'cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'],
                                                                                               filename,
                                                                                               data['bs']), ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout('0.0.0.0', 'user2', '1111', 'cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ''):
        return None, None
    if not ssh_checkout('0.0.0.0', 'user2', '1111',
                        'cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'],
                                                                                                  subfoldername,
                                                                                                  testfilename,
                                                                                                  data['bs']), ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def make_bad_arx():
    ssh_checkout('0.0.0.0', 'user2', '1111',
                 'cd {}; 7z a {}/bad_arx -t{}'.format(data['folder_in'], data['folder_out'], data['type']),
                 'Everything '
                 'is Ok')
    ssh_checkout('0.0.0.0', 'user2', '1111', 'truncate -s 1 {}/bad_arx.{}'.format(data['folder_out'], data['type']), '')


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
    yield
    print('Finish: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout('cat /proc/loadavg')
    ssh_checkout('0.0.0.0', 'user2', '1111', 'echo "time: {} count: {} size: {} load: {}">> stat.txt'.format(
        datetime.now().strftime('%H:%M:%S.%f'), data['count'], data['bs'], stat), '')


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files('0.0.0.0', 'user2', '1111', '/home/user/p7zip-full.deb',
                 '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout('0.0.0.0', 'user2', '1111', 'echo "1111" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(
        ssh_checkout('0.0.0.0', 'user2', '1111', 'echo "1111" | sudo -S dpkg -s p7zip-full.deb', 'Status: install ok '
                                                                                                 'installed'))
    return all(res)


@pytest.fixture(autouse=True)
def start_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@pytest.fixture(autouse=True)
def save_log():
    with open('log.txt', 'w') as f:
        f.write(ssh_get('0.0.0.0', 'user2', '1111', 'echo "1111" | sudo -S journalctl --since "{}">> stat.txt'.format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))


@pytest.fixture(autouse=True)
def ll():
    yield
    slg = ssh_get('0.0.0.0', 'user2', '1111', 'journalctl --since "{}"'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    ssh_checkout('0.0.0.0', 'user2', '1111', 'echo load: "{}">> kj.txt'.format(
        slg), '')
